from unittest.mock import patch

from raincheck_simpler import get_current_weather_info, get_daily_weather_forecast
from raincheck_simpler.models import CurrentWeatherInfo, DailyForecastInfo


def test_get_current_weather_info_ok_response():

    mock_response = {
        "current_condition": [
            {
                "temp_C": "22",
                "humidity": "42",
                "windspeedKmph": "8",
                "precipMM": "0.0",
                "weatherDesc": [{"value": "Partly cloudy"}],
            }
        ]
    }

    expoected_result = CurrentWeatherInfo(
        location_name="TestCity",
        temperature_C=22,
        humidity=42,
        wind_speed_kph=8,
        precipitation_mm=0.0,
        condition="Partly cloudy",
    )

    with patch(
        "raincheck_simpler.services.fetch_weather", return_value=mock_response
    ):
        result = get_current_weather_info("TestCity")

    assert result == expoected_result


def test_get_daily_weather_forecast_ok_response():

    mock_response = {
        "weather": [
            {
                "date": "2023-10-01",
                "avgtempC": "20",
                "maxtempC": "25",
                "mintempC": "15",
            },
            {
                "date": "2023-10-02",
                "avgtempC": "21",
                "maxtempC": "26",
                "mintempC": "16",
            },
            {
                "date": "2023-10-03",
                "avgtempC": "19",
                "maxtempC": "24",
                "mintempC": "14",
            },
        ]
    }

    expected_result = [
        DailyForecastInfo(
            date="2023-10-01",
            avg_temperature_C=20,
            max_temperature_C=25,
            min_temperature_C=15,
        ),
        DailyForecastInfo(
            date="2023-10-02",
            avg_temperature_C=21,
            max_temperature_C=26,
            min_temperature_C=16,
        ),
        DailyForecastInfo(
            date="2023-10-03",
            avg_temperature_C=19,
            max_temperature_C=24,
            min_temperature_C=14,
        ),
    ]

    with patch(
        "raincheck_simpler.services.fetch_weather", return_value=mock_response
    ):
        result = get_daily_weather_forecast("TestCity")

    assert result == expected_result
