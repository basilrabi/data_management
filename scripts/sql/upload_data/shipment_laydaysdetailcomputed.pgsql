CREATE TEMPORARY TABLE temp_shipment_laydaysdetailcomputed
(
    interval_class character varying(50),
    interval_from timestamp with time zone,
    laytime_rate smallint,
    remarks text,
    time_remaining interval,
    name character varying(10)
);

\copy temp_shipment_laydaysdetailcomputed FROM 'data/shipment_laydaysdetailcomputed.csv' DELIMITER ',' CSV;

INSERT INTO shipment_laydaysdetailcomputed (
    interval_class,
    interval_from,
    laytime_rate,
    remarks,
    time_remaining,
    laydays_id
)
SELECT
    a.interval_class,
    a.interval_from,
    a.laytime_rate,
    a.remarks,
    a.time_remaining,
    c.id
FROM temp_shipment_laydaysdetailcomputed a
    LEFT JOIN shipment_shipment b
        ON a.name = b.name
    LEFT JOIN shipment_laydaysstatement c
        ON b.id = c.shipment_id;
