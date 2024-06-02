SELECT
    city_id,
    name,
    latitude,
    longitude,
    city_type_id
FROM
    public.city
WHERE
    name = :city_name;