INSERT INTO
    public.daily_historical_weather (
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