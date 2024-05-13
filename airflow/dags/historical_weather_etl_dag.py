import numpy as np
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from api.database_api import WeatherDatabaseAPI
from api.open_meteo_api import OpenMeteoAPI
from config.settings import load_cities
from config.settings import load_weather_format

default_args = {
    "owner": "your_name",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "historical_weather_etl",
    default_args=default_args,
    description="Extract, Transform, Load historical weather data",
    schedule_interval="@weekly",
)

cities = load_cities()
weather_format = load_weather_format()
db_api = WeatherDatabaseAPI(db_type="postgresql")


def extract_historical_weather_for_city(city, start_date, end_date, daily):
    """Extract historical weather data for a specific city and date range."""
    api = OpenMeteoAPI(latitude=city["latitude"], longitude=city["longitude"])
    data = api.get_historical_weather(start_date, end_date, daily=daily)
    return {"city": city["name"], "data": data}


def transform_and_load_historical_weather(**kwargs):
    """Transform and load historical weather data for all cities."""
    start_date = weather_format["start_date"]
    end_date = weather_format["end_date"]
    if end_date == "today":
        end_date = datetime.now().date().isoformat()
    daily = False
    frequency = weather_format["data_frequency"]
    if frequency == "daily":
        daily = True

    for city in cities:
        weather_data = extract_historical_weather_for_city(
            city, start_date, end_date, daily=daily
        )
        # Implement transformation logic here to align with the database schema
        transformed_data = transform_historical_weather(
            city_name=city["name"], weather_data=weather_data, daily=daily
        )

        for entry in transformed_data:
            if daily:
                db_api.insert_daily_historical_weather(**entry)
            else:
                db_api.insert_hourly_historical_weather(**entry)


def transform_historical_weather(city_name, weather_data, daily):
    """
    Transform the current weather data to match the database schema.

    Args:
        city_name (str): The ID of the city in the database.
        weather_data (dict): The raw data from the Open-Meteo API.

    Returns:
        dict: Transformed data for the `current_weather` table.
    """
    entries = []
    if daily:
        historical_weather = weather_data["data"]["daily"]

        # Extract and convert the fields
        timestamps_list = historical_weather["time"]
        timestamps = [datetime.fromisoformat(t) for t in timestamps_list]
        temperatures_max = historical_weather["temperature_2m_max"]
        temperatures_min = historical_weather["temperature_2m_min"]
        temperatures_avg = np.round(
            (np.array(temperatures_max) + np.array(temperatures_min)) / 2, 1
        )
        wind_speeds_10m = historical_weather["wind_speed_10m_max"]
        precipitation_sums = historical_weather["precipitation_sum"]

        for ts, t_max, t_min, t_avg, ws, pc in zip(
            timestamps,
            temperatures_max,
            temperatures_min,
            temperatures_avg,
            wind_speeds_10m,
            precipitation_sums,
        ):
            entries.append(
                {
                    "city_name": city_name,
                    "date": ts,
                    "temperature_max": t_max,
                    "temperature_min": t_min,
                    "temperature_avg": t_avg,
                    "precipitation_sum": pc,
                    "wind_speed_10m": ws,
                }
            )
    else:
        historical_weather = weather_data["data"]["hourly"]

        # Extract and convert the fields
        timestamps_list = historical_weather["time"]
        timestamps = [datetime.fromisoformat(t) for t in timestamps_list]
        temperatures = historical_weather["temperature_2m"]
        wind_speeds_10m = historical_weather["wind_speed_10m"]
        precipitations = historical_weather["precipitation"]
        humidities = historical_weather["relative_humidity_2m"]

        for ts, tmp, ws, pc, hu in zip(
            timestamps, temperatures, wind_speeds_10m, precipitations, humidities
        ):
            entries.append(
                {
                    "city_name": city_name,
                    "timestamp": ts,
                    "temperature": tmp,
                    "precipitation": pc,
                    "wind_speed_10m": ws,
                    "humidity": hu,
                }
            )
    return entries


load_historical_task = PythonOperator(
    task_id="load_historical_weather",
    python_callable=transform_and_load_historical_weather,
    dag=dag,
    provide_context=True,
)

load_historical_task
