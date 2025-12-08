"""Demo of TMDB SDK with dataclass responses."""

import os

from tmdb_sdk.client import TMDBClient


try:
    from dotenv import load_dotenv
except ImportError:
    pass  # не е задължително проектът ви да изисква `python-dotenv`
    # сложили сме го само за ваше удобство
else:
    load_dotenv()


def demo():
    """This is just a sample demo of your TMDB SDK expected functionality."""

    api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        print("Error: Please set TMDB_API_KEY environment variable")
        print("export TMDB_API_KEY='your_api_key_here'")
        return

    client = TMDBClient(api_key)

    # ========== SDK CALLS ==========
    # Example 1: Most popular movies
    popular = client.discover_movies(
        language="en-US", sort_by="popularity.desc", limit=5
    )

    # Example 2: Best rated movies from 2025
    movies_2025 = client.discover_movies(
        year=2025,
        sort_by="vote_average.desc",
        limit=5,
    )

    # Example 3: Search for 'Inception' movie(s)
    search_results = client.search_movies("Inception", limit=3)

    # Example 4: Get all movie genres
    genres = client.get_movie_genres()

    # Example 5: Filter by the genres (comedy AND action)
    comedy = next(g for g in genres if g.name == "Comedy")
    action = next(g for g in genres if g.name == "Action")

    comedy_movies = client.discover_movies(
        genres=comedy & action,
        sort_by="popularity.desc",
        limit=5,
    )

    # Example 6: Most popular series shows
    series_shows = client.discover_series(sort_by="popularity.desc", limit=5)

    # ========== DISPLAY RESULTS ==========
    print("\n=== Popular Movies ===")
    for movie in popular:
        print(f"  - {movie.title} (Rating: {movie.vote_average})")

    print("\n=== 2025 Best Rated Movies ===")
    for movie in movies_2025:
        print(f"  - {movie.title} (Rating: {movie.vote_average})")

    print("\n=== Search: 'Inception' ===")
    for movie in search_results:
        year = movie.release_date[:4] if movie.release_date else "N/A"
        print(f"  - {movie.title} ({year})")

    print("\n=== Movie Genres ===")
    print(f"  Found {len(genres)} genres:")
    for genre in genres:
        print(f"    {genre.id}: {genre.name}")

    print(f"\n=== Action Comedy Movies ===")
    for movie in comedy_movies:
        print(f"  - {movie.title} (Rating: {movie.vote_average})")

    print("\n=== Popular Series Shows ===")
    for show in series_shows:
        print(f"  - {show.name} (Rating: {show.vote_average})")

    print("\n=== Complete! ===")


if __name__ == "__main__":
    demo()
