INSERT INTO
    public.historical_weather_daily (
        city_id,
        date,
        temperature_min,
        temperature_max,
        temperature_avg,
        precipitation_sum,
        wind_speed_max
    )
VALUES
    (
        :city_id,
        :date,
        :temperature_min,
        :temperature_max,
        :temperature_avg,
        :precipitation_sum,
        :wind_speed_max
    );