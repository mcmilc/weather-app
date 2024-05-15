SELECT
    weather_id,
    city_id,
    timestamp,
    temperature,
    precipitation,
    humidity,
    wind_speed_10m
FROM
    public.historical_weather_hourly
WHERE
    city_id = :city_id
    AND date BETWEEN :start_date
    AND :end_date;