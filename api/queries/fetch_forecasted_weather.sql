SELECT
    weather_id,
    city_id,
    forecast_date,
    temperature,
    precipitation,
    humidity,
    wind_speed,
FROM
    public.forecasted_weather
WHERE
    city_id = :city_id;