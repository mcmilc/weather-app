INSERT INTO
    public.historical_weather (
        city_id,
        date,
        temperature,
        precipitation,
        wind_speed
    )
VALUES
    (
        :city_id,
        :date,
        :temperature,
        :precipitation,
        :wind_speed
    );