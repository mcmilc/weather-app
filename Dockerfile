# Base image
FROM python:3.11 as base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Build API package
FROM base as builder
COPY api /app/api
COPY config /app/config
RUN install_packages.sh

# Dash-specific setup
FROM base as dash-setup
COPY dash_app /app/dash_app
COPY start_dash_app.sh /app/start_dash_app.sh

# Airflow-specific setup
FROM base as airflow-setup
COPY airflow /app/airflow