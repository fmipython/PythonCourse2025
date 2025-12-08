"""Unit tests for TMDB SDK."""

import pytest
from unittest.mock import Mock, patch
from tmdb_sdk.client import TMDBClient
from tmdb_sdk.models import Movie, Series, Genre, GenreQuery
from tmdb_sdk.exceptions import (
    TMDBException,
    TMDBAuthenticationError,
    TMDBNotFoundError,
    TMDBRateLimitError,
    TMDBServerError,
)


@pytest.fixture
def client() -> TMDBClient:
    """Create a TMDBClient instance for unit testing."""
    return TMDBClient("test_api_key")


class TestTMDBClientInit:
    """Test TMDBClient initialization and basic functionality."""

    def test_init_without_api_key(self):
        """Test client initialization without API key raises ValueError."""
        with pytest.raises(ValueError, match="API key is required"):
            TMDBClient(None)  # type: ignore

        with pytest.raises(ValueError, match="API key is required"):
            TMDBClient("")


class TestGenreOperations:
    """Test Genre and GenreQuery operator overloading."""

    def test_genre_or_operator(self):
        """Test OR operator (|) for Genre objects."""
        action = Genre(id=28, name="Action")
        comedy = Genre(id=35, name="Comedy")

        result = action | comedy

        assert isinstance(result, GenreQuery)
        assert str(result) == "28|35"

    def test_genre_and_operator(self):
        """Test AND operator (&) for Genre objects."""
        action = Genre(id=28, name="Action")
        comedy = Genre(id=35, name="Comedy")

        result = action & comedy

        assert isinstance(result, GenreQuery)
        assert str(result) == "28,35"

    def test_genre_chaining_or(self):
        """Test chaining multiple genres with OR operator."""
        action = Genre(id=28, name="Action")
        comedy = Genre(id=35, name="Comedy")
        drama = Genre(id=18, name="Drama")

        result = action | comedy | drama

        assert isinstance(result, GenreQuery)
        assert str(result) == "28|35|18"

    def test_genre_chaining_and(self):
        """Test chaining multiple genres with AND operator."""
        action = Genre(id=28, name="Action")
        comedy = Genre(id=35, name="Comedy")
        drama = Genre(id=18, name="Drama")

        result = action & comedy & drama

        assert isinstance(result, GenreQuery)
        assert str(result) == "28,35,18"


class TestDiscoverMovies:
    """Test discover_movies method."""

    @patch("requests.Session.get")
    def test_discover_movies_basic(self, mock_get, client):
        """Test basic discover movies request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [{"id": 111, "title": "Test Movie"}],
            "total_pages": 1,
            "total_results": 1,
        }
        mock_get.return_value = mock_response

        result = client.discover_movies()

        assert len(result) == 1
        assert result[0].id == 111
        assert result[0].title == "Test Movie"

    @patch("requests.Session.get")
    def test_discover_movies_parse_all_fields(self, mock_get, client):
        """Test that all fields are parsed correctly in discover movies."""
        expoected_result = [
            Movie(
                id=146,
                title="Crouching Tiger, Hidden Dragon",
                vote_average=7.434,
                original_title="卧虎藏龍",
                overview="Two warriors in pursuit of a stolen sword and a notorious fugitive are led to an impetuous, physically-skilled, teenage nobleman's daughter, who is at a crossroads in her life.",
                release_date="2000-07-06",
                poster_path="/iNDVBFNz4XyYzM9Lwip6atSTFqf.jpg",
                backdrop_path="/nSm9cij9VRrGDoZoS16CPnX0FqK.jpg",
                genre_ids=[12, 18, 28, 10749],
                popularity=4.7894,
                vote_count=3432,
                adult=False,
                original_language="zh",
                video=False,
            ),
        ]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [
                {
                    "id": 146,
                    "title": "Crouching Tiger, Hidden Dragon",
                    "vote_average": 7.434,
                    "original_title": "卧虎藏龍",
                    "overview": "Two warriors in pursuit of a stolen sword and a notorious fugitive are led to an impetuous, physically-skilled, teenage nobleman's daughter, who is at a crossroads in her life.",
                    "release_date": "2000-07-06",
                    "poster_path": "/iNDVBFNz4XyYzM9Lwip6atSTFqf.jpg",
                    "backdrop_path": "/nSm9cij9VRrGDoZoS16CPnX0FqK.jpg",
                    "genre_ids": [12, 18, 28, 10749],
                    "popularity": 4.7894,
                    "vote_count": 3432,
                    "adult": False,
                    "original_language": "zh",
                    "video": False,
                }
            ],
            "total_pages": 1,
            "total_results": 1,
        }
        mock_get.return_value = mock_response

        result = client.discover_movies()

        assert result == expoected_result

    @patch("requests.Session.get")
    def test_discover_movies_with_filters(self, mock_get, client):
        """Test discover movies with filters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [],
            "page": 1,
            "total_pages": 1,
            "total_results": 0,
        }
        mock_get.return_value = mock_response

        action = Genre(id=28, name="Action")
        adventure = Genre(id=12, name="Adventure")

        client.discover_movies(
            language="bg-BG",
            region="BG",
            sort_by="popularity.desc",
            year=2025,
            genres=action & adventure,
            limit=5,
        )

        args, kwargs = mock_get.call_args
        params = kwargs["params"]
        assert params["language"] == "bg-BG"
        assert params["region"] == "BG"
        assert params["sort_by"] == "popularity.desc"
        assert params["year"] == 2025
        assert params["with_genres"] == "28,12"
        assert params["page"] == 1
        assert "limit" not in params

    @patch("requests.Session.get")
    def test_discover_movies_genre_none(self, mock_get, client):
        """Test discover_movies with genres=None."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [],
            "page": 1,
            "total_pages": 1,
            "total_results": 0,
        }
        mock_get.return_value = mock_response

        client.discover_movies(genres=None)

        args, kwargs = mock_get.call_args
        assert "with_genres" not in kwargs["params"]

    @patch("requests.Session.get")
    def test_discover_movies_auto_pagination(self, mock_get, client):
        """Test discover movies with auto-pagination."""

        # create mock responses for multiple pages
        def side_effect(*args, **kwargs):
            page = kwargs["params"]["page"]
            mock_response = Mock()
            mock_response.status_code = 200
            if page == 1:
                mock_response.json.return_value = {
                    "results": [{"id": i, "title": f"Movie {i}"} for i in range(1, 21)],
                    "page": 1,
                    "total_pages": 3,
                    "total_results": 60,
                }
            elif page == 2:
                mock_response.json.return_value = {
                    "results": [
                        {"id": i, "title": f"Movie {i}"} for i in range(21, 41)
                    ],
                    "page": 2,
                    "total_pages": 3,
                    "total_results": 60,
                }
            return mock_response

        mock_get.side_effect = side_effect

        result = client.discover_movies(limit=30)

        assert mock_get.call_count == 2
        assert len(result) == 30


class TestExceptions:
    """Test custom exception handling in TMDBClient."""

    @patch("requests.Session.get")
    def test_authentication_error(self, mock_get, client):
        """Test handling of authentication error (401)."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with pytest.raises(TMDBAuthenticationError):
            client.discover_movies()
        with pytest.raises(TMDBAuthenticationError):
            client.discover_series()
        with pytest.raises(TMDBAuthenticationError):
            client.search_movies("Test")
        with pytest.raises(TMDBAuthenticationError):
            client.search_series("Test")

    @patch("requests.Session.get")
    def test_not_found_error(self, mock_get, client):
        """Test handling of not found error (404)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(TMDBNotFoundError):
            client.discover_movies()
        with pytest.raises(TMDBNotFoundError):
            client.discover_series()
        with pytest.raises(TMDBNotFoundError):
            client.search_movies("Test")
        with pytest.raises(TMDBNotFoundError):
            client.search_series("Test")

    @patch("requests.Session.get")
    def test_rate_limit_error(self, mock_get, client):
        """Test handling of rate limit error (429)."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        with pytest.raises(TMDBRateLimitError):
            client.discover_movies()
        with pytest.raises(TMDBRateLimitError):
            client.discover_series()
        with pytest.raises(TMDBRateLimitError):
            client.search_movies("Test")
        with pytest.raises(TMDBRateLimitError):
            client.search_series("Test")

    @patch("requests.Session.get")
    def test_server_error(self, mock_get, client):
        """Test handling of server error (5xx)."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(TMDBServerError):
            client.discover_movies()
        with pytest.raises(TMDBServerError):
            client.discover_series()
        with pytest.raises(TMDBServerError):
            client.search_movies("Test")
        with pytest.raises(TMDBServerError):
            client.search_series("Test")

    @patch("requests.Session.get")
    def test_generic_exception(self, mock_get, client):
        """Test handling of generic request exceptions."""
        mock_response = Mock()
        mock_response.status_code = 418  # I'm a teapot
        mock_get.return_value = mock_response

        with pytest.raises(TMDBException):
            client.discover_movies()
        with pytest.raises(TMDBException):
            client.discover_series()
        with pytest.raises(TMDBException):
            client.search_movies("Test")
        with pytest.raises(TMDBException):
            client.search_series("Test")

    def test_genre_with_invalid_type(self, client):
        """Test that passing invalid type to genres raises TypeError."""
        with pytest.raises(TypeError):
            client.discover_movies(genres="invalid")  # type: ignore

        with pytest.raises(TypeError):
            client.discover_movies(genres=123)  # type: ignore

        with pytest.raises(TypeError):
            client.discover_series(genres=[1, 2, 3])  # type: ignore

    def test_discover_movies_invalid_limit(self, client):
        """Test that an invalid limit raises ValueError."""
        with pytest.raises(ValueError):
            client.discover_movies(limit=-1)
        with pytest.raises(ValueError):
            client.discover_series(limit=-1)
        with pytest.raises(ValueError):
            client.search_movies("Test", limit=-1)
        with pytest.raises(ValueError):
            client.search_series("Test", limit=-1)
