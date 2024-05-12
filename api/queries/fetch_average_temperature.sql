SELECT
    date,
    AVG(temperature) as avg_temperature
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