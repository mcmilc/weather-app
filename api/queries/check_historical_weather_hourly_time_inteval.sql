WITH OrderedData AS (
    SELECT
        weather_id,
        city_id,
        timestamp,
        LAG(timestamp) OVER (
            PARTITION BY city_id
            ORDER BY
                timestamp
        ) AS previous_timestamp
    FROM
        public.historical_weather_hourly
),
TimeDiffs AS (
    SELECT
        weather_id,
        city_id,
        timestamp,
        previous_timestamp,
        EXTRACT(
            EPOCH
            FROM
                (timestamp - previous_timestamp)
        ) / 3600 AS hours_diff -- Difference in hours
    FROM
        OrderedData
)
SELECT
    weather_id,
    city_id,
    timestamp,
    previous_timestamp,
    hours_diff
FROM
    TimeDiffs
WHERE
    hours_diff != 1
    AND previous_timestamp IS NOT NULL -- Checking for gaps not equal to 1 hour
ORDER BY
    city_id,
    timestamp;