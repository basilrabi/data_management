SELECT
    shipment_lct.name,
    shipment_vessel.name,
    shipment_trip.status,
    shipment_trip.dump_truck_trips,
    shipment_trip.vessel_grab,
    shipment_trip.interval_from
FROM shipment_trip
    LEFT JOIN shipment_lct
        ON shipment_trip.lct_id = shipment_lct.id
    LEFT JOIN shipment_vessel
        ON shipment_trip.vessel_id = shipment_vessel.id
ORDER BY
    shipment_lct.name,
    shipment_trip.interval_from,
    shipment_vessel.name
