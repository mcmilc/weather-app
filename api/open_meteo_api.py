import pycurl
import json
from io import BytesIO
from urllib.parse import urlencode


class OpenMeteoAPI:
    # Base URLs for each type of data
    URLS = {
        "current": "https://api.open-meteo.com/v1/",
        "forecast": "https://api.open-meteo.com/v1/",
        "historical": "https://archive-api.open-meteo.com/v1/",
    }

    def __init__(self, latitude, longitude):
        """Initialize with the geographic coordinates of interest."""
        self.latitude = latitude
        self.longitude = longitude

    def _fetch_data(self, endpoint, params, data_type):
        """Fetch data from the specified endpoint using given parameters."""
        buffer = BytesIO()
        curl = pycurl.Curl()
        base_url = self.URLS.get(
            data_type, "https://api.open-meteo.com/v1/"
        )  # Fallback to the default URL
        url = f"{base_url}{endpoint}?{urlencode(params)}"
        print(f"Fetching data from URL: {url}")  # Debug statement to see the full URL
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEFUNCTION, buffer.write)
        curl.perform()
        curl.close()
        data = buffer.getvalue().decode("utf-8")
        return json.loads(data)

    def get_current_weather(self):
        """Get current weather data."""
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
        }
        return self._fetch_data("forecast", params, "current")

    def get_historical_weather(self, start_date, end_date):
        """Get historical weather data for a given date range."""
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        }
        return self._fetch_data("archive", params, "historical")

    def get_forecasted_weather(self, daily=True):
        """Get weather forecast data."""
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
            if daily
            else "",
            "hourly": "temperature_2m,precipitation" if not daily else "",
        }
        return self._fetch_data("forecast", params, "forecast")


if __name__ == "__main__":
    api = OpenMeteoAPI(
        latitude=33.8699, longitude=-118.3911
    )  # Example coordinates for Manhattan Beach

    # Current Weather
    current_weather = api.get_current_weather()
    print("Current Weather:", current_weather)

    # Historical Weather
    # historical_weather = api.get_historical_weather(
    #    start_date="2024-01-01", end_date="2024-01-31"
    # )
    # print("Historical Weather:", historical_weather)

    # Forecasted Weather
    # forecasted_weather = api.get_forecasted_weather(daily=True)
    # print("Forecasted Weather:", forecasted_weather)
