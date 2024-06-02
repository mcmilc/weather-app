INSERT INTO
    public.current_weather (
        city_id,
        timestamp,
        temperature,
        precipitation,
        humidity,
        wind_speed
    )
VALUES
    (
        :city_id,
        :timestamp,
        :temperature,
        :precipitation,
        :humidity,
        :wind_speed
    );