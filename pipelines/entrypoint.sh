#!/bin/bash

echo "Waiting for database..."
/app/wait-for-it.sh airflow_db:5432 --timeout=30 --strict -- echo "Airflow DB is up."
echo "Starting Airflow..."
airflow db migrate

# Check if the user already exists
if ! airflow users list | grep -q "airflow_web_user"; then
    echo "Creating Airflow user..."
    airflow users create \
        --username airflow_web_user \
        --password airflowpassword \
        --firstname Airflow \
        --lastname User \
        --role Admin \
        --email airflow@example.com
    echo "Airflow user created."
else
    echo "Airflow user already exists."
fi

exec "$@"