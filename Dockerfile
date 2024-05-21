# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt setup.py install_packages.sh /app/
RUN chmod +x /app/install_packages.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/wait-for-it.sh

# Run the install_packages.sh to install api and config as packages
COPY api /app/api
COPY config /app/config
RUN /app/install_packages.sh

# Copy the dash_app directory and start_dash_app.sh script
COPY dash_app ./dash_app
COPY start_dash_app.sh ./

# Ensure the script is executable
RUN chmod +x ./start_dash_app.sh

# Arguments to pass UID and GID
ARG UID=1000
ARG GID=1000

# Setup Airflow directories, user, and group
RUN groupadd --gid ${GID} airflow && \
    useradd --uid ${UID} --gid ${GID} --create-home --home-dir /opt/airflow --shell /bin/bash airflow && \
    mkdir -p /opt/airflow/logs /opt/airflow/logs/scheduler && \
    chown -R airflow:airflow /opt/airflow

# Airflow setup and user ang group creation
# RUN addgroup --system airflow && adduser --system --ingroup airflow airflow

RUN mkdir -p /opt/airflow
RUN mkdir -p /opt/airflow/logs
RUN mkdir -p /opt/airflow/logs/scheduler
RUN mkdir -p /opt/airflow/dags

COPY airflow /opt/airflow
COPY --chown=airflow:airflow airflow.cfg /opt/airflow/airflow.cfg
COPY --chown=airflow:airflow webserver_config.py /opt/airflow/webserver_config.py

RUN chmod 644 /opt/airflow/airflow.cfg
RUN chmod 644 /opt/airflow/webserver_config.py
RUN chown -R airflow:airflow /opt/airflow/logs
RUN chown -R airflow:airflow /opt/airflow/logs/scheduler
RUN chmod 775 /opt/airflow
RUN chmod 775 /opt/airflow/logs
RUN chmod 775 /opt/airflow/logs/scheduler
RUN chmod 775 /opt/airflow/dags

USER airflow

COPY airflow/dags /opt/airflow/dags 