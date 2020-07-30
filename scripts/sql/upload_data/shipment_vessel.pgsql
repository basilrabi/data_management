CREATE TEMPORARY TABLE temp_shipment_vessel
(
    name character varying(50),
    stripped_name character varying(50)
);

\copy temp_shipment_vessel FROM 'data/shipment_vessel.csv' DELIMITER ',' CSV;

INSERT INTO shipment_vessel (name, stripped_name)
SELECT name, stripped_name
FROM temp_shipment_vessel
