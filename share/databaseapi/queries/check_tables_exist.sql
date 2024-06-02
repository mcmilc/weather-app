-- check_tables_exist.sql
SELECT
    tablename
FROM
    pg_tables
WHERE
    schemaname = :schema
    AND tablename IN :table_names;