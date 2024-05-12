INSERT INTO
    public.daily_historical_weather (
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