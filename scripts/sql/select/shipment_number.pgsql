CREATE MATERIALIZED VIEW shipment_number AS
WITH raw_stamps AS (
    SELECT
        a.id,
        a.name,
        b.arrival_tmc,
        b.completed_loading,
        MAX(c.interval_from) last_detail
    FROM shipment_shipment a
        LEFT JOIN shipment_laydaysstatement b
            ON a.id = b.shipment_id
        LEFT JOIN shipment_laydaysdetail c
            ON b.id = c.laydays_id
    GROUP BY
        a.id,
        a.name,
        b.arrival_tmc,
        b.completed_loading
),
coalesced_stamps AS (
    SELECT
        id,
        arrival_tmc,
        completed_loading,
        last_detail,
        name,
        COALESCE(
            last_detail,
            arrival_tmc,
            '2100-01-01 00:00:00'::timestamp
        ) time_stamp
    FROM raw_stamps
),
year_added AS (
    SELECT *, DATE_TRUNC('year', time_stamp) year_begin
    FROM coalesced_stamps
),
numbered AS (
    SELECT
        id,
        EXTRACT(YEAR FROM time_stamp)::text the_year,
        ROW_NUMBER () OVER (
            PARTITION BY year_begin
            ORDER BY
                completed_loading ASC NULLS LAST,
                arrival_tmc ASC NULLS LAST,
                last_detail ASC NULLS LAST,
                name ASC
        ) shipment_number
    FROM year_added
)
SELECT
    id shipment_id,
    the_year || '-' || LPAD(shipment_number::text, 2, '0') number
FROM numbered
