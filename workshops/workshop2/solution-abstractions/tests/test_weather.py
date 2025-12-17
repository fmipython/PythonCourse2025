import pytest

from raincheck_abstractions import Weather
from raincheck_abstractions.models import CurrentWeatherInfo, DailyForecastInfo


@pytest.fixture
def mock_current_weather_info() -> CurrentWeatherInfo:
    return CurrentWeatherInfo(
        location_name="MockCity",
        temperature_C=25.0,
        humidity=50.0,
        wind_speed_kph=10.0,
        precipitation_mm=5.0,
        condition="Sunny",
    )


@pytest.fixture
def mock_daily_forecast_info() -> list[DailyForecastInfo]:
    return [
        DailyForecastInfo(
            date="2024-01-01",
            avg_temperature_C=20.0,
            max_temperature_C=25.0,
            min_temperature_C=15.0,
        ),
        DailyForecastInfo(
            date="2024-01-02",
            avg_temperature_C=22.0,
            max_temperature_C=27.0,
            min_temperature_C=17.0,
        ),
    ]


@pytest.fixture(autouse=True)
def mock_service(mock_current_weather_info, mock_daily_forecast_info):
    global _REGISTRY

    from raincheck_abstractions.services.base import WeatherServiceBase
    from raincheck_abstractions.services.registry import _REGISTRY

    class WttrinServiceMock(WeatherServiceBase):
        def get_current_weather_info(self, location: str) -> CurrentWeatherInfo:
            return mock_current_weather_info

        def get_daily_weather_forecast(self, location: str) -> list[DailyForecastInfo]:
            return mock_daily_forecast_info

    _REGISTRY["MOCK"] = WttrinServiceMock

    return WttrinServiceMock()


def test_mock_current_weather_info(mock_current_weather_info):
    weather = Weather("MOCK")
    current_info = weather.current("TEST LOCATION")
    assert current_info == mock_current_weather_info


def test_mock_daily_forecast_info(mock_daily_forecast_info):
    weather = Weather("MOCK")
    daily_info = weather.daily_forecast("TEST LOCATION")
    assert daily_info == mock_daily_forecast_info
