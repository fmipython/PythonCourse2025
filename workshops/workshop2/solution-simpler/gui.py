import streamlit as st

from raincheck_simpler import get_current_weather_info, get_daily_weather_forecast


def display_current_weather(location: str):
    weather_info = get_current_weather_info(location)

    st.header(f"Current Weather in {weather_info.location_name}")
    st.metric(label="Temperature (°C)", value=weather_info.temperature_C)
    st.metric(label="Humidity (%)", value=weather_info.humidity)
    st.metric(label="Wind Speed (km/h)", value=weather_info.wind_speed_kph)
    st.metric(label="Precipitation (mm)", value=weather_info.precipitation_mm)
    st.write(f"Condition: {weather_info.condition}")


def display_daily_forecast(location: str):
    forecast_info = get_daily_weather_forecast(location)

    st.header(f"Daily Weather Forecast for {location}")
    for day in forecast_info:
        st.subheader(day.date)
        st.metric(label="Max Temperature (°C)", value=day.max_temperature_C)
        st.metric(label="Avg Temperature (°C)", value=day.avg_temperature_C)
        st.metric(label="Min Temperature (°C)", value=day.min_temperature_C)
        st.markdown("---")


def main():
    st.title("RainCheck Weather App")

    location = st.text_input("Enter Location", "Sofia")

    if st.button("Get Current Weather"):
        display_current_weather(location)

    if st.button("Get Daily Forecast"):
        display_daily_forecast(location)


if __name__ == "__main__":
    main()
