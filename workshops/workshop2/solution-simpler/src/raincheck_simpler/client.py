import requests


_WEATHER_API_URL = "https://wttr.in/{city}"

def fetch_weather(location: str) -> dict:
    response = requests.get(
        _WEATHER_API_URL.format(city=location),
        params={"format": "j1"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
