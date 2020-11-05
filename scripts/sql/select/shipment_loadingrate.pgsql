CREATE MATERIALIZED VIEW shipment_loadingrate AS
WITH cte_a AS (
    SELECT
        shipment.name shipment,
        ldstatement.tonnage,
        COALESCE(
            lddetail.interval_from, ldstatement.arrival_tmc
        ) AS interval_start,
        COALESCE(lat_a.interval_from, date_trunc('hour', NOW())) interval_end
    FROM shipment_shipment shipment
        LEFT JOIN shipment_laydaysstatement ldstatement
            ON ldstatement.shipment_id = shipment.id
        LEFT JOIN shipment_laydaysdetail lddetail
            ON lddetail.laydays_id = ldstatement.id
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_laydaysdetail temp_tab
            WHERE temp_tab.laydays_id = lddetail.laydays_id
                AND temp_tab.interval_from > lddetail.interval_from
            ORDER BY temp_tab.interval_from
            LIMIT 1
        ) lat_a ON true
    WHERE lddetail.interval_from IS NULL
        OR lddetail.interval_class = 'continuous loading'
),
cte_b AS (
    SELECT
        shipment,
        tonnage,
        gs interval_start
    FROM cte_a,
        generate_series(
            interval_start,
            interval_end - '1 minute'::interval,
            '1 minute'::interval
        ) gs
),
cte_c AS (
    SELECT
        shipment,
        tonnage,
        date_trunc('day', interval_start) date,
        COUNT(*) minute_elapsed
    FROM cte_b
    GROUP BY shipment, tonnage, date_trunc('day', interval_start)
),
cte_d AS (
    SELECT
        tonnage,
        date,
        minute_elapsed,
        SUM(minute_elapsed) OVER(PARTITION BY shipment) total_minutes
    FROM cte_c
),
cte_e AS (
    SELECT
        date,
        tonnage::float * minute_elapsed::float / total_minutes::float wmt
    FROM cte_d
),
cte_f AS (
    SELECT date loading_date, SUM(wmt) wmt
    FROM cte_e
    GROUP BY date
),
cte_g as (
    SELECT generate_series(
        MIN(loading_date),
        MAX(loading_date),
        '1 day'::interval
    ) loading_date
    FROM cte_f
)
SELECT
    cte_g.loading_date::date,
    COALESCE(cte_f.wmt, 0) wmt
FROM cte_g
    LEFT JOIN cte_f
        ON cte_f.loading_date = cte_g.loading_date
