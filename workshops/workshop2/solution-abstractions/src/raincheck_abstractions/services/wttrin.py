import requests

from raincheck_abstractions.models import CurrentWeatherInfo, DailyForecastInfo
from raincheck_abstractions.services.base import WeatherServiceBase


_WEATHER_API_URL = "https://wttr.in/{city}"


class WttrinWeatherService(WeatherServiceBase):
    def get_current_weather_info(self, location: str) -> CurrentWeatherInfo:
        weather_data = self._make_request(location)
        return self._parse_current_weather(weather_data, location)

    def get_daily_weather_forecast(self, location: str) -> list[DailyForecastInfo]:
        weather_data = self._make_request(location)
        return self._parse_daily_forecast(weather_data)

    def _make_request(self, location: str) -> dict:
        response = requests.get(
            _WEATHER_API_URL.format(city=location),
            params={"format": "j1"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def _parse_current_weather(self, data: dict, location: str) -> CurrentWeatherInfo:
        current_condition = data["current_condition"][0]
        return CurrentWeatherInfo(
            location_name=location,
            temperature_C=float(current_condition["temp_C"]),
            humidity=float(current_condition["humidity"]),
            wind_speed_kph=float(current_condition["windspeedKmph"]),
            precipitation_mm=float(current_condition.get("precipMM", 0.0)),
            condition=current_condition["weatherDesc"][0]["value"],
        )

    def _parse_daily_forecast(self, data: dict) -> list[DailyForecastInfo]:
        forecast_data = data["weather"]
        return [
            DailyForecastInfo(
                date=day["date"],
                avg_temperature_C=float(day["avgtempC"]),
                max_temperature_C=float(day["maxtempC"]),
                min_temperature_C=float(day["mintempC"]),
            )
            for day in forecast_data
        ]
