SELECT
    weather_id,
    city_id,
    date,
    temperature,
    precipitation,
    wind_speed_10m
FROM
    public.forecasted_weather_daily
WHERE
    city_id = :city_id;