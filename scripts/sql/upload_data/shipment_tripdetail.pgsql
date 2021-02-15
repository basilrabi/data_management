CREATE TEMPORARY TABLE temp_shipment_tripdetail
(
    name character varying(50),
    trip_start timestamp with time zone,
    detail timestamp with time zone,
    interval_class character varying(30),
    remarks text
);

\copy temp_shipment_tripdetail FROM 'data/shipment_tripdetail.csv' DELIMITER ',' CSV;

INSERT INTO shipment_tripdetail (
    interval_from, interval_class, remarks, trip_id
)
SELECT
    temp_shipment_tripdetail.detail,
    temp_shipment_tripdetail.interval_class,
    temp_shipment_tripdetail.remarks,
    shipment_trip.id
FROM temp_shipment_tripdetail
    LEFT JOIN shipment_lct
        ON temp_shipment_tripdetail.name = shipment_lct.name
    LEFT JOIN shipment_trip
        ON shipment_lct.id = shipment_trip.lct_id
            AND temp_shipment_tripdetail.trip_start = shipment_trip.interval_from
GROUP BY
    temp_shipment_tripdetail.detail,
    temp_shipment_tripdetail.interval_class,
    temp_shipment_tripdetail.remarks,
    shipment_trip.id
