import openmeteo_requests
import pandas as pd
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("laundry")


@mcp.tool()
async def get_fabric_types() -> list[str]:
    return ["light-fabrics", "typical-fabrics", "heavy-fabrics"]


@mcp.tool()
async def get_preferred_drying_method() -> str:
    return "line-drying"


@mcp.tool()
async def get_forecast(latitude: float, longitude: float, timezone: str) -> list[dict]:
    om = openmeteo_requests.AsyncClient()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "precipitation_probability",
            "wind_speed_10m",
            "wind_direction_10m",
            "uv_index"
        ],
        "timezone": timezone,
    }
    responses = await om.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(6).ValuesAsNumpy()

    hourly_data = {
        "datetime": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "temperature_2m": hourly_temperature_2m,
        "relative_humidity_2m": hourly_relative_humidity_2m,
        "precipitation": hourly_precipitation,
        "precipitation_probability": hourly_precipitation_probability,
        "wind_speed_10m": hourly_wind_speed_10m,
        "wind_direction_10m": hourly_wind_direction_10m,
        "uv_index": hourly_uv_index,
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe = hourly_dataframe.head(24 * 3)
    hourly_dataframe["datetime"] = hourly_dataframe["datetime"].dt.tz_convert(timezone)

    return hourly_dataframe.to_dict("records")


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
