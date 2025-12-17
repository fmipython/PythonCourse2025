# тук можете да наследите WeatherServiceBase за да имплементирате OpenMeteo-специфична логика

# import openmeteo_sdk - тежък импорт

from raincheck_abstractions.models import CurrentWeatherInfo, DailyForecastInfo
from raincheck_abstractions.services.base import WeatherServiceBase


class OpenMeteoWeatherService(WeatherServiceBase):
    def get_current_weather_info(self, location: str) -> CurrentWeatherInfo:
        # dummy implementation
        return CurrentWeatherInfo(
            location_name=location,
            temperature_C=0.0,
            humidity=0.0,
            wind_speed_kph=0.0,
            precipitation_mm=0.0,
            condition="Unknown",
        )

    def get_daily_weather_forecast(self, location: str) -> list[DailyForecastInfo]:
        # dummy implementation
        return [
            DailyForecastInfo(
                date="2026-01-01",
                avg_temperature_C=0.0,
                max_temperature_C=0.0,
                min_temperature_C=0.0,
            ),
        ]
