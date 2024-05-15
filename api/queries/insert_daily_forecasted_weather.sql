INSERT INTO
    public.forecasted_weather_daily (
        city_id,
        date,
        temperature,
        precipitation,
        wind_speed_10m
    )
VALUES
    (
        :city_id,
        :date,
        :temperature,
        :precipitation,
        :wind_speed_10m
    );