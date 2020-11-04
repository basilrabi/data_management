CREATE MATERIALIZED VIEW shipment_loadingrate AS
WITH cte_a AS (
    SELECT
        shipment.name shipment,
        ldstatement.tonnage,
        ldstatement.arrival_tmc::date arrival,
        COALESCE(lat_a.interval_from::date, now()::date) departure
    FROM shipment_shipment shipment
        LEFT JOIN shipment_laydaysstatement ldstatement
            ON ldstatement.shipment_id = shipment.id
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_laydaysdetail lddetail
            WHERE lddetail.laydays_id = ldstatement.id
            ORDER BY interval_from DESC
            LIMIT 1
        ) lat_a ON true
),
cte_b AS (
    SELECT *,
        tonnage::float / (1 + departure - arrival)::float daily_rate
    FROM cte_a
    WHERE tonnage IS NOT NULL
),
cte_c AS (
    SELECT *,
        generate_series(
            arrival::timestamp,
            departure::timestamp,
            '1 day'::interval
        )::date loading_date
    FROM cte_b
),
cte_d AS (
    SELECT generate_series(
        MIN(arrival)::timestamp,
        MAX(departure)::timestamp,
        '1 day'::interval
    )::date loading_date
    FROM cte_b
),
cte_e AS (
    SELECT loading_date, SUM(daily_rate) wmt
    FROM cte_c
    GROUP BY loading_date
),
cte_f AS (
    SELECT
        cte_d.loading_date,
        COALESCE(cte_e.wmt, 0) wmt
    FROM cte_d
        LEFT JOIN cte_e
            ON cte_e.loading_date = cte_d.loading_date
),
cte_g AS (
    SELECT cte_f.*,
        lat_b.wmt previous_wmt,
        lat_c.wmt next_wmt
    FROM cte_f
        LEFT JOIN LATERAL (
            SELECT wmt
            FROM cte_f temp_tab
            WHERE temp_tab.loading_date < cte_f.loading_date
            ORDER BY temp_tab.loading_date DESC
            LIMIT 1
        ) lat_b ON true
        LEFT JOIN LATERAL (
            SELECT wmt
            FROM cte_f temp_tab
            WHERE temp_tab.loading_date > cte_f.loading_date
            ORDER BY temp_tab.loading_date ASC
            LIMIT 1
        ) lat_c ON true
)
SELECT loading_date, wmt
FROM cte_g
WHERE wmt <> previous_wmt
    OR wmt <> next_wmt
    OR next_wmt IS NULL
    OR previous_wmt IS NULL
ORDER BY loading_date
