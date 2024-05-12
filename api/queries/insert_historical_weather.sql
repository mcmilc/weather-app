INSERT INTO
    public.historical_weather (
        city_id,
        date,
        temperature,
        precipitation,
        humidity,
        wind_speed
    )
VALUES
    (
        :city_id,
        :date,
        :temperature,
        :precipitation,
        :humidity,
        :wind_speed
    );