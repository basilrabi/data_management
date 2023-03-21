WITH a AS (
    SELECT
        shipment_lct.name,
        MIN(shipment_tripdetail.interval_from) OVER (PARTITION BY shipment_tripdetail.trip_id) trip_start,
        shipment_tripdetail.interval_from detail,
        shipment_tripdetail.interval_class,
        shipment_tripdetail.remarks,
        COUNT(*) OVER (PARTITION BY shipment_tripdetail.trip_id) siblings
    FROM shipment_tripdetail
        LEFT JOIN shipment_trip
            ON shipment_tripdetail.trip_id = shipment_trip.id
        LEFT JOIN shipment_lct
            ON shipment_trip.lct_id = shipment_lct.id
    ORDER BY
        shipment_tripdetail.interval_from,
        shipment_trip.interval_from,
        shipment_lct.name
)
SELECT
    a.name,
    a.trip_start,
    a.detail,
    a.interval_class,
    a.remarks
FROM a
WHERE siblings > 1
