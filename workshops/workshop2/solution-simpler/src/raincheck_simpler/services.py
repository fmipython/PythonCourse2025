from raincheck_simpler.client import fetch_weather
from raincheck_simpler.models import CurrentWeatherInfo, DailyForecastInfo


def get_current_weather_info(location: str) -> CurrentWeatherInfo:
    weather_data = fetch_weather(location)
    current_condition = weather_data["current_condition"][0]

    return CurrentWeatherInfo(
        location_name=location,
        temperature_C=float(current_condition["temp_C"]),
        humidity=float(current_condition["humidity"]),
        wind_speed_kph=float(current_condition["windspeedKmph"]),
        precipitation_mm=float(current_condition.get("precipMM", 0.0)),
        condition=current_condition["weatherDesc"][0]["value"],
    )


def get_daily_weather_forecast(location: str) -> list[DailyForecastInfo]:
    weather_data = fetch_weather(location)
    forecast_data = weather_data["weather"]

    forecast_list = [
        DailyForecastInfo(
            date=day["date"],
            avg_temperature_C=float(day["avgtempC"]),
            max_temperature_C=float(day["maxtempC"]),
            min_temperature_C=float(day["mintempC"]),
        )
        for day in forecast_data
    ]

    return forecast_list
