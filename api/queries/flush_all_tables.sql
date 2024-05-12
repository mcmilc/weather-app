DELETE FROM
    public.city;

DELETE FROM
    public.city_type;

DELETE FROM
    public.forecasted_weather;

DELETE FROM
    public.historical_weather;

DELETE FROM
    public.current_weather;

ALTER SEQUENCE forecasted_weather_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE historical_weather_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE current_weather_weather_id_seq RESTART WITH 1;

ALTER SEQUENCE city_type_city_type_id_seq RESTART WITH 1;

ALTER SEQUENCE city_city_id_seq RESTART WITH 1;