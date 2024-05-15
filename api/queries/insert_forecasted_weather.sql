INSERT INTO
    public.forecasted_weather_daily (
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