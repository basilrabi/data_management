SELECT
    c.name,
    a.anchored,
    a.latitude_degree,
    a.latitude_minutes,
    a.longitude_degree,
    a.longitude_minutes
FROM location_anchorage a
    LEFT JOIN shipment_laydaysstatement b
        ON a.laydays_id = b.id
    LEFT JOIN shipment_shipment c
        ON b.shipment_id = c.id
ORDER BY
    b.completed_loading,
    c.name,
    a.anchored
