from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from api.open_meteo_api import OpenMeteoAPI
from api.database_api import WeatherDatabaseAPI
from config.settings import load_json

default_args = {
    "owner": "your_name",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "forecasted_weather_etl",
    default_args=default_args,
    description="Extract, Transform, Load forecasted weather data",
    schedule_interval="@daily",
)

cities = load_json("config/cities.json")["cities"]
db_api = WeatherDatabaseAPI(db_type="postgresql")


def extract_forecasted_weather_for_city(city):
    """Extract forecasted weather data for a specific city."""
    api = OpenMeteoAPI(latitude=city["latitude"], longitude=city["longitude"])
    data = api.get_forecasted_weather()
    return {"city": city["name"], "data": data}


def transform_and_load_forecasted_weather(**kwargs):
    """Transform and load forecasted weather data for all cities."""
    for city in cities:
        weather_data = extract_forecasted_weather_for_city(city)
        # Implement transformation logic here to align with the database schema
        transformed_data = transform_forecasted_weather(
            city_name=city, weather_data=weather_data
        )  # Replace with your transformation code

        for entry in transformed_data:
            db_api.insert_forecasted_weather(**entry)


def transform_forecasted_weather(city_name, weather_data):
    """
    Transform the current weather data to match the database schema.

    Args:
        city_name (str): The ID of the city in the database.
        weather_data (dict): The raw data from the Open-Meteo API.

    Returns:
        dict: Transformed data for the `current_weather` table.
    """
    forecasted_weather = weather_data["Forecasted Weather"]["daily"]

    # Extract and convert the fields
    timestamp_str = forecasted_weather["time"]
    timestamp = datetime.fromisoformat(timestamp_str)

    temperature = forecasted_weather["temperature_2m_max"]
    wind_speed = forecasted_weather["wind_speed_10m_max"]
    precipitation = forecasted_weather["precipitation_sum"]
    return {
        "name": city_name,
        "timestamp": timestamp,
        "temperature": temperature,
        "precipitation": precipitation,
        "wind_speed": wind_speed,
    }


load_forecasted_task = PythonOperator(
    task_id="load_forecasted_weather",
    python_callable=transform_and_load_forecasted_weather,
    dag=dag,
    provide_context=True,
)

load_forecasted_task
