SELECT
    weather_id,
    city_id,
    timestamp,
    temperature,
    precipitation,
    humidity,
    wind_speed
FROM
    public.current_weather
WHERE
    city_id = :city_id