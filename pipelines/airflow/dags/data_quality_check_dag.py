from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from databaseapi.api import WeatherDatabaseAPI


def check_tables_exist():
    db = WeatherDatabaseAPI(db_type="postgresql")
    tables_exist = db.check_tables_exist()
    if tables_exist:
        Variable.set("tables_exist", "true")
    else:
        Variable.set("tables_exist", "false")
        raise ValueError("Tables exist data quality check failed")


def check_data_quality_historical_weather():
    db = WeatherDatabaseAPI(db_type="postgresql")
    tables_exist = db.check_tables_exist()
    has_conform_rows = db.check_data_quality_historical_weather_hourly()
    quality_passed = tables_exist and has_conform_rows
    if quality_passed:
        Variable.set("historical_weather_quality_passed", "true")
    else:
        Variable.set("historical_weather_quality_passed", "false")
        raise ValueError("Historical weather data quality check failed")


default_args = {
    "owner": "MCMilc",
    "start_date": days_ago(1),
}

dag = DAG(
    "data_quality_check",
    default_args=default_args,
    schedule=timedelta(days=1),  # Adjust as needed
)

check_tables_exist_task = PythonOperator(
    task_id="check_tables_exist",
    python_callable=check_tables_exist,
    dag=dag,
)

check_data_quality_historical_weather_task = PythonOperator(
    task_id="check_data_quality_historical_weather",
    python_callable=check_data_quality_historical_weather,
    dag=dag,
)

check_tables_exist_task >> check_data_quality_historical_weather_task
