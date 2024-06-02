# Use an official Python runtime as a parent image
FROM python:3.11

# Argument to specify the dependencies directory
ARG PROJECT_DIR

# Set the working directory in the container
WORKDIR /app

# Install python requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install shared dependencies
COPY share /app/share
COPY ./install_packages.sh /app/share/install_packages.sh
RUN chmod +x /app/share/install_packages.sh
WORKDIR /app/share
RUN /app/share/install_packages.sh
WORKDIR /app

# Copy the dags directory
COPY ./pipelines/entrypoint.sh /app/entrypoint.sh
COPY ./wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/wait-for-it.sh

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

COPY ./pipelines/airflow /opt/airflow
COPY --chown=airflow:airflow ./pipelines/airflow.cfg /opt/airflow/airflow.cfg
COPY --chown=airflow:airflow ./pipelines/webserver_config.py /opt/airflow/webserver_config.py

RUN chmod 644 /opt/airflow/airflow.cfg
RUN chmod 644 /opt/airflow/webserver_config.py
RUN chown -R airflow:airflow /opt/airflow/logs
RUN chown -R airflow:airflow /opt/airflow/logs/scheduler
RUN chmod 775 /opt/airflow
RUN chmod 775 /opt/airflow/logs
RUN chmod 775 /opt/airflow/logs/scheduler
RUN chmod 775 /opt/airflow/dags

USER airflow

COPY ./pipelines/airflow/dags /opt/airflow/dags 