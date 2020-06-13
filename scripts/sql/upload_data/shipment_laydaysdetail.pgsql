CREATE TEMPORARY TABLE temp_shipment_laydaysdetail
(
    name character varying(10),
    interval_from timestamp with time zone,
    laytime_rate smallint,
    interval_class character varying(50),
    remarks text
);

\copy temp_shipment_laydaysdetail FROM 'data/shipment_laydaysdetail.csv' DELIMITER ',' CSV;

INSERT INTO shipment_laydaysdetail (
    interval_from,
    laytime_rate,
    interval_class,
    remarks,
    laydays_id
)
SELECT
    temp_shipment_laydaysdetail.interval_from,
    temp_shipment_laydaysdetail.laytime_rate,
    temp_shipment_laydaysdetail.interval_class,
    temp_shipment_laydaysdetail.remarks,
    shipment_laydaysstatement.id
FROM temp_shipment_laydaysdetail
    LEFT JOIN shipment_shipment
        ON temp_shipment_laydaysdetail.name = shipment_shipment.name
    LEFT JOIN shipment_laydaysstatement
        ON shipment_shipment.id = shipment_laydaysstatement.shipment_id;
