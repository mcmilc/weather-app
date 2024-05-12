from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from api.database_api import WeatherDatabaseAPI
from api.open_meteo_api import OpenMeteoAPI
from config.settings import load_cities
from config.settings import load_date_range

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
date_range = load_date_range()
db_api = WeatherDatabaseAPI(db_type="postgresql")


def extract_historical_weather_for_city(city, start_date, end_date):
    """Extract historical weather data for a specific city and date range."""
    api = OpenMeteoAPI(latitude=city["latitude"], longitude=city["longitude"])
    data = api.get_historical_weather(start_date, end_date)
    return {"city": city["name"], "data": data}


def transform_and_load_historical_weather(**kwargs):
    """Transform and load historical weather data for all cities."""
    start_date = date_range["start_date"]
    end_date = date_range["end_date"]
    for city in cities:
        weather_data = extract_historical_weather_for_city(city, start_date, end_date)
        # Implement transformation logic here to align with the database schema
        transformed_data = transform_historical_weather(
            city_name=city["name"], weather_data=weather_data
        )

        for entry in transformed_data:
            db_api.insert_historical_weather(**entry)


def transform_historical_weather(city_name, weather_data):
    """
    Transform the current weather data to match the database schema.

    Args:
        city_name (str): The ID of the city in the database.
        weather_data (dict): The raw data from the Open-Meteo API.

    Returns:
        dict: Transformed data for the `current_weather` table.
    """

    historical_weather = weather_data["data"]["daily"]

    # Extract and convert the fields
    timestamps_list = historical_weather["time"]
    timestamps = [datetime.fromisoformat(t) for t in timestamps_list]
    temperatures = historical_weather["temperature_2m_max"]
    wind_speeds = historical_weather["wind_speed_10m_max"]
    precipitations = historical_weather["precipitation_sum"]

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


load_historical_task = PythonOperator(
    task_id="load_historical_weather",
    python_callable=transform_and_load_historical_weather,
    dag=dag,
    provide_context=True,
)

load_historical_task
