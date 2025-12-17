from abc import ABC, abstractmethod

from raincheck_abstractions.models import CurrentWeatherInfo, DailyForecastInfo


class WeatherServiceBase(ABC):
    @abstractmethod
    def get_current_weather_info(self, location: str) -> CurrentWeatherInfo: ...

    @abstractmethod
    def get_daily_weather_forecast(self, location: str) -> list[DailyForecastInfo]: ...
