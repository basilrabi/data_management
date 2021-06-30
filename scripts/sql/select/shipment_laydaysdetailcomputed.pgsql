SELECT
    a.interval_class,
    a.interval_from,
    a.laytime_rate,
    a.remarks,
    a.time_remaining,
    c.name
FROM shipment_laydaysdetailcomputed a
    LEFT JOIN shipment_laydaysstatement b
        ON a.laydays_id = b.id
    LEFT JOIN shipment_shipment c
        ON b.shipment_id = c.id
ORDER BY
    b.completed_loading,
    c.name,
    a.interval_from
