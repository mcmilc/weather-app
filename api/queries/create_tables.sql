BEGIN;

CREATE TABLE IF NOT EXISTS PUBLIC.city_type (
    city_type_id SERIAL PRIMARY KEY,
    city_type VARCHAR(50) NOT NULL,
    UNIQUE (city_type) -- Unique constraint for city type
);

CREATE TABLE IF NOT EXISTS PUBLIC.city (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    city_type_id INTEGER REFERENCES city_type(city_type_id),
    UNIQUE (name, latitude, longitude) -- Unique constraint for city name, latitude, and longitude
);

CREATE TABLE IF NOT EXISTS PUBLIC.historical_weather_daily (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    date DATE NOT NULL,
    temperature_max FLOAT,
    temperature_min FLOAT,
    temperature_avg FLOAT,
    precipitation_sum FLOAT,
    wind_speed_max FLOAT,
    UNIQUE (city_id, date)
);

CREATE TABLE IF NOT EXISTS PUBLIC.historical_weather_hourly (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    timestamp TIMESTAMPTZ NOT NULL,
    temperature FLOAT,
    precipitation FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    UNIQUE (city_id, datetime)
);

CREATE TABLE IF NOT EXISTS PUBLIC.current_weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    timestamp TIMESTAMPTZ NOT NULL,
    temperature FLOAT,
    precipitation FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    UNIQUE (city_id, timestamp) -- Unique constraint for city and timestamp
);

CREATE TABLE IF NOT EXISTS PUBLIC.forecasted_weather_daily (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES city(city_id),
    date DATE NOT NULL,
    temperature FLOAT,
    precipitation FLOAT,
    wind_speed FLOAT,
    UNIQUE (city_id, date) -- Unique constraint for city and forecast date
);

COMMIT;