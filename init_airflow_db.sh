#!/bin/bash
set -e

# Wait for MySQL to start
echo "Waiting for MySQL..."
while ! mysqladmin ping -h"mysql" --silent; do
    sleep 1
done
echo "MySQL started"

# Login to MySQL and configure database and user
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    CREATE DATABASE IF NOT EXISTS airflow_db;
    CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflowpassword';
    GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow'@'%';
    FLUSH PRIVILEGES;
EOSQL
