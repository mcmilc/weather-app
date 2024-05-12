SELECT
    date,
    AVG(wind_speed) as avg_wind_speed
FROM
    public.historical_weather
WHERE
    city_id = :city_id
    AND date BETWEEN :start_date
    AND :end_date
GROUP BY
    date
ORDER BY
    date;