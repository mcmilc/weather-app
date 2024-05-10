from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from api.database_api import WeatherDatabaseAPI
from api.open_meteo_api import OpenMeteoAPI
from config.settings import load_json

default_args = {
    "owner": "your_name",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "current_weather_etl",
    default_args=default_args,
    description="Extract, Transform, Load current weather data",
    schedule_interval="@hourly",
)

cities = load_json("config/cities.json")["cities"]
db_api = WeatherDatabaseAPI(db_type="postgresql")


def extract_current_weather_for_city(city):
    """Extract current weather data for a specific city."""
    api = OpenMeteoAPI(latitude=city["latitude"], longitude=city["longitude"])
    data = api.get_current_weather()
    return {"city": city["name"], "data": data}


def transform_and_load_current_weather(**kwargs):
    """Transform and load current weather data for all cities."""
    for city in cities:
        weather_data = extract_current_weather_for_city(city)
        # Implement transformation logic here to align with the database schema
        transformed_data = transform_current_weather(
            city_name=city, weather_data=weather_data
        )

        for entry in transformed_data:
            db_api.insert_current_weather(**entry)


def transform_current_weather(city_name, weather_data):
    """
    Transform the current weather data to match the database schema.

    Args:
        city_name (str): The ID of the city in the database.
        weather_data (dict): The raw data from the Open-Meteo API.

    Returns:
        dict: Transformed data for the `current_weather` table.
    """
    current_weather = weather_data["Current Weather"]

    # Extract and convert the fields
    timestamp_str = current_weather["time"]
    timestamp = datetime.fromisoformat(timestamp_str)

    temperature = current_weather["temperature_2m"]
    wind_speed = current_weather["wind_speed_10m"]
    precipitation = current_weather["precipitation"]
    humidity = current_weather["relative_humidity_2m"]
    # Return the transformed data
    return {
        "name": city_name,
        "timestamp": timestamp,
        "temperature": temperature,
        "precipitation": precipitation,  # Assuming no data available in this API
        "humidity": humidity,  # Assuming no data available in this API
        "wind_speed": wind_speed,
    }


load_current_task = PythonOperator(
    task_id="load_current_weather",
    python_callable=transform_and_load_current_weather,
    dag=dag,
    provide_context=True,
)

load_current_task
