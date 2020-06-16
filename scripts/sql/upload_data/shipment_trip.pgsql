CREATE TEMPORARY TABLE temp_shipment_trip
(
    lct character varying(50),
    vessel character varying(50),
    status character varying(20),
    dump_truck_trips smallint,
    vessel_grab smallint,
    interval_from timestamp with time zone
);

\copy temp_shipment_trip FROM 'data/shipment_trip.csv' DELIMITER ',' CSV;

INSERT INTO shipment_trip (
    status,
    dump_truck_trips,
    vessel_grab,
    interval_from,
    valid,
    continuous,
    lct_id,
    vessel_id
)
SELECT
    temp_shipment_trip.status,
    temp_shipment_trip.dump_truck_trips,
    temp_shipment_trip.vessel_grab,
    temp_shipment_trip.interval_from,
    false,
    false,
    shipment_lct.id,
    shipment_vessel.id
FROM temp_shipment_trip
    LEFT JOIN shipment_lct
        ON temp_shipment_trip.lct = shipment_lct.name
    LEFT JOIN shipment_vessel
        ON temp_shipment_trip.vessel = shipment_vessel.name;
