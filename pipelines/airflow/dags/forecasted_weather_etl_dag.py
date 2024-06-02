from weatherapi.api import OpenMeteoAPI
from databaseapi.api import WeatherDatabaseAPI
from config.readers import load_cities
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta

default_args = {
    "owner": "MCMilc",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "forecasted_weather_etl",
    default_args=default_args,
    description="Extract, Transform, Load forecasted weather data",
    schedule=timedelta(days=1),
)


def extract_forecasted_weather_for_city(city):
    """Extract forecasted weather data for a specific city."""
    api = OpenMeteoAPI(latitude=city["latitude"], longitude=city["longitude"])
    data = api.get_forecasted_weather()
    return {"city": city["name"], "data": data}


def transform_and_load_forecasted_weather(**kwargs):
    """Transform and load forecasted weather data for all cities."""
    cities = load_cities()
    db_api = WeatherDatabaseAPI(db_type="postgresql")
    for city in cities:
        weather_data = extract_forecasted_weather_for_city(city)
        # Implement transformation logic here to align with the database schema
        transformed_data = transform_forecasted_weather(
            city_name=city["name"], weather_data=weather_data
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
    forecasted_weather = weather_data["data"]["daily"]

    # Extract and convert the fields
    timestamps_list = forecasted_weather["time"]
    timestamps = [datetime.fromisoformat(t) for t in timestamps_list]
    temperatures = forecasted_weather["temperature_2m_max"]
    wind_speeds = forecasted_weather["wind_speed_10m_max"]
    precipitations = forecasted_weather["precipitation_sum"]

    entries = []
    for ts, tm, ws, pc in zip(timestamps, temperatures, wind_speeds, precipitations):
        entries.append(
            {
                "city_name": city_name,
                "date": ts,
                "temperature": tm,
                "precipitation": pc,
                "wind_speed": ws,
            }
        )
    return entries


load_forecasted_task = PythonOperator(
    task_id="load_forecasted_weather",
    python_callable=transform_and_load_forecasted_weather,
    dag=dag,
    provide_context=True,
)

load_forecasted_task
