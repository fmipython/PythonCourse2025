from rich.console import Console
from rich.table import Table
import typer

from raincheck_simpler import get_current_weather_info, get_daily_weather_forecast


app = typer.Typer()


@app.command()
def current(location: str):
    weather_info = get_current_weather_info(location)

    table = Table(title=f"Current Weather in {weather_info.location_name}")
    table.add_column("Temperature (°C)", justify="right")
    table.add_column("Humidity (%)", justify="right")
    table.add_column("Wind Speed (km/h)", justify="right")
    table.add_column("Precipitation (mm)", justify="right")
    table.add_column("Condition", justify="left")

    table.add_row(
        f"{weather_info.temperature_C}",
        f"{weather_info.humidity}",
        f"{weather_info.wind_speed_kph}",
        f"{weather_info.precipitation_mm}",
        weather_info.condition,
    )
    console = Console()
    console.print(table)


@app.command()
def daily(location: str):
    forecast_info = get_daily_weather_forecast(location)

    table = Table(title=f"Daily Weather Forecast for {location}")
    table.add_column("Date", justify="left")
    table.add_column("Max Temp (°C)", justify="right")
    table.add_column("Avg Temp (°C)", justify="right")
    table.add_column("Min Temp (°C)", justify="right")

    for day in forecast_info:
        table.add_row(
            day.date,
            f"{day.max_temperature_C}",
            f"{day.avg_temperature_C}",
            f"{day.min_temperature_C}",
        )
    console = Console()
    console.print(table)


if __name__ == "__main__":
    app()
