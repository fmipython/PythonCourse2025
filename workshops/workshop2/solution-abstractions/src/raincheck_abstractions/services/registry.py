from enum import StrEnum

from raincheck_abstractions.services.base import WeatherServiceBase
from raincheck_abstractions.services.wttrin import WttrinWeatherService
from raincheck_abstractions.services.openmeteo import OpenMeteoWeatherService


class WeatherProvider(StrEnum):
    WTTRIN = "wttrin"
    OPENMETEO = "openmeteo"


DEFAULT_PROVIDER = WeatherProvider.WTTRIN


_REGISTRY: dict[str, type[WeatherServiceBase]] = {
    WeatherProvider.WTTRIN: WttrinWeatherService,
    WeatherProvider.OPENMETEO: OpenMeteoWeatherService,
}


def get_weather_service(provider_name: str) -> WeatherServiceBase:
    provider_class = _REGISTRY.get(provider_name)
    if not provider_class:
        raise ValueError(f"Unknown weather provider: {provider_name}")

    return provider_class()  # инстанцираме конкретния клас
