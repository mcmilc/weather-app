BEGIN;

CREATE TABLE IF NOT EXISTS PUBLIC.city_type (
    city_type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS PUBLIC.city (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    city_type_id INTEGER REFERENCES city_type(city_type_id),
    UNIQUE (name, latitude, longitude)  -- Unique constraint for city details
);

CREATE TABLE IF NOT EXISTS PUBLIC.historical_weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    date DATE NOT NULL,
    temperature FLOAT,
    precipitation FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    UNIQUE (city_id, date)  -- Unique constraint for city and date
);

CREATE TABLE IF NOT EXISTS PUBLIC.current_weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    timestamp TIMESTAMPTZ NOT NULL,
    temperature FLOAT,
    precipitation FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    UNIQUE (city_id, timestamp)  -- Unique constraint for city and timestamp
);

CREATE TABLE IF NOT EXISTS PUBLIC.forecasted_weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    forecast_date DATE NOT NULL,
    temperature FLOAT,
    precipitation FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    UNIQUE (city_id, forecast_date)  -- Unique constraint for city and forecast date
);

COMMIT;