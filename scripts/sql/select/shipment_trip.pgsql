WITH cte  AS (
    SELECT
        shipment_trip.id,
        shipment_trip.lct_id,
        shipment_vessel.name vessel,
        shipment_trip.status,
        shipment_trip.dump_truck_trips,
        shipment_trip.vessel_grab,
        min_time.interval_from,
        max_time.interval_to,
        shipment_set.shipment_set > 0 AS valid
    FROM shipment_trip
        LEFT JOIN shipment_vessel
            ON shipment_trip.vessel_id = shipment_vessel.id
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_tripdetail
            WHERE trip_id = shipment_trip.id
            ORDER BY interval_from ASC
            LIMIT 1
        ) min_time ON true
        LEFT JOIN LATERAL (
            SELECT interval_from interval_to
            FROM shipment_tripdetail
            WHERE trip_id = shipment_trip.id
                AND interval_from > min_time.interval_from
            ORDER BY interval_from DESC
            LIMIT 1
        ) max_time ON true
        LEFT JOIN LATERAL (
            SELECT COUNT(*) shipment_set
            FROM shipment_shipment
                LEFT JOIN shipment_laydaysstatement
                    ON shipment_shipment.id = shipment_laydaysstatement.shipment_id
            WHERE shipment_shipment.vessel_id = shipment_trip.vessel_id
                AND shipment_laydaysstatement.commenced_loading <= max_time.interval_to
                AND (
                    shipment_laydaysstatement.completed_loading IS NULL
                        OR shipment_laydaysstatement.completed_loading >= min_time.interval_from
                )
        ) shipment_set ON true
)
SELECT
    shipment_lct.name lct,
    cte.vessel,
    cte.status,
    cte.dump_truck_trips,
    cte.vessel_grab,
    cte.interval_from,
    cte.interval_to,
    cte.valid,
    CASE
        WHEN cte.interval_to IS NULL THEN false
        WHEN cte.interval_from <> previous_trip.interval_to THEN false
        WHEN cte.interval_to <> next_trip.interval_from THEN false
        ELSE true
    END continuous
FROM cte
    LEFT JOIN shipment_lct
        ON shipment_lct.id = cte.lct_id
    LEFT JOIN LATERAL (
        SELECT interval_to
        FROM cte trip_list
        WHERE trip_list.id <> cte.id
            AND trip_list.lct_id = cte.lct_id
            AND trip_list.interval_from < cte.interval_from
        ORDER BY interval_from DESC
        LIMIT 1
    ) previous_trip ON true
    LEFT JOIN LATERAL (
        SELECT interval_from
        FROM cte trip_list
        WHERE trip_list.id <> cte.id
            AND trip_list.lct_id = cte.lct_id
            AND trip_list.interval_from > cte.interval_from
        ORDER BY interval_from ASC
        LIMIT 1
    ) next_trip ON true
WHERE cte.interval_from IS NOT NULL
    AND cte.interval_to IS NOT NULL
ORDER BY
    shipment_lct.name,
    cte.interval_from,
    cte.vessel
