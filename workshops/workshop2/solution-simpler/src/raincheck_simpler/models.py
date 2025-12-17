from dataclasses import dataclass


@dataclass
class CurrentWeatherInfo:
    location_name: str
    temperature_C: float
    humidity: float
    wind_speed_kph: float
    precipitation_mm: float
    condition: str


@dataclass
class DailyForecastInfo:
    date: str
    avg_temperature_C: float
    max_temperature_C: float
    min_temperature_C: float
