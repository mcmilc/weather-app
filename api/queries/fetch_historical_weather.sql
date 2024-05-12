SELECT
    weather_id,
    city_id,
    date,
    temperature,
    precipitation,
    humidity,
    wind_speed
FROM
    public.historical_weather
WHERE
    city_id = :city_id
    AND date BETWEEN :start_date
    AND :end_date;