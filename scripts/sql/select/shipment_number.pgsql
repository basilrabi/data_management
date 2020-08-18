CREATE MATERIALIZED VIEW shipment_number AS
WITH aa as (
    SELECT
        a.id,
        a.name,
        b.arrival_tmc date_a,
        MAX(c.interval_from) date_b
    FROM shipment_shipment a
    LEFT JOIN shipment_laydaysstatement b
        ON a.id = b.shipment_id
    LEFT JOIN shipment_laydaysdetail c
        ON b.id = c.laydays_id
    GROUP BY a.id, a.name, b.arrival_tmc
),
bb as (
    SELECT
        id, name,
        COALESCE(date_b, date_a, '2100-01-01 00:00:00'::timestamp) time_stamp
    FROM aa
),
cc as (
    SELECT *, date_trunc('year', bb.time_stamp) year_begin
    FROM bb
),
dd as (
    SELECT
        id, time_stamp, EXTRACT(YEAR FROM time_stamp)::text the_year,
        ROW_NUMBER () OVER (PARTITION BY year_begin ORDER BY time_stamp, name) shipment_number
    FROM cc
)
SELECT
    id shipment_id,
    the_year || '-' || LPAD(shipment_number::text, 2, '0') number
FROM dd
