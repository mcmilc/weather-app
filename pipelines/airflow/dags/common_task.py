from airflow.operators.python import PythonOperator
from airflow.models import Variable


def verify_tables_exist():
    quality_passed = Variable.get("tables_exist")
    if quality_passed != "true":
        raise ValueError("Table exist quality check did not pass")


def verify_data_quality_historical_weather():
    quality_passed = Variable.get("historical_weather_quality_passed")
    if quality_passed != "true":
        raise ValueError("Historical weather quality check did not pass")


def create_verify_data_quality_historical_weather_task(dag):
    return PythonOperator(
        task_id="verify_data_quality_historical_weather",
        python_callable=verify_data_quality_historical_weather,
        dag=dag,
    )


def create_verify_tables_exist(dag):
    return PythonOperator(
        task_id="verify_tables_exist",
        python_callable=verify_tables_exist,
        dag=dag,
    )
