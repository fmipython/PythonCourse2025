"""Описва основния клас на библиотеката."""

from raincheck_abstractions.models import CurrentWeatherInfo, DailyForecastInfo
from raincheck_abstractions.services.registry import (
    DEFAULT_PROVIDER,
    get_weather_service,
    WeatherProvider,
)


class Weather:
    def __init__(self, provider_name: WeatherProvider | None = None):
        if provider_name is None:
            provider_name = DEFAULT_PROVIDER
        self._service = get_weather_service(provider_name)

    def current(self, location: str) -> CurrentWeatherInfo:
        return self._service.get_current_weather_info(location)

    def daily_forecast(self, location: str) -> list[DailyForecastInfo]:
        return self._service.get_daily_weather_forecast(location)
