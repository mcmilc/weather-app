INSERT INTO
    public.historical_weather_hourly (
        city_id,
        timestamp,
        temperature,
        precipitation,
        humidity,
        wind_speed_10m
    )
VALUES
    (
        :city_id,
        :timestamp,
        :temperature,
        :precipitation,
        :humidity,
        :wind_speed_10m
    );