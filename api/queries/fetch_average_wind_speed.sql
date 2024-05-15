SELECT
    DATE(timestamp) AS date,
    ROUND(AVG(wind_speed_10m) :: numeric, 1) AS avg_wind_speed
FROM
    PUBLIC.historical_weather_hourly
WHERE
    timestamp BETWEEN :start_date
    AND :end_date
    AND city_id = :city_id
GROUP BY
    DATE(timestamp)
ORDER BY
    DATE(timestamp);