DELETE FROM
    public.city;

DELETE FROM
    public.city_type;

DELETE FROM
    public.forecasted_weather_daily;

DELETE FROM
    public.historical_weather_daily;

DELETE FROM
    public.historical_weather_hourly;

DELETE FROM
    public.current_weather;

ALTER SEQUENCE forecasted_weather_daily_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE historical_weather_hourly_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE historical_weather_daily_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE current_weather_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE city_type_city_type_id_seq RESTART WITH 1;

ALTER SEQUENCE city_city_id_seq RESTART WITH 1;