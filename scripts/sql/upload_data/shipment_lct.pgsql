CREATE TEMPORARY TABLE temp_shipment_lct
(
    name character varying(50),
    capacity smallint
);

\copy temp_shipment_lct FROM 'data/shipment_lct.csv' DELIMITER ',' CSV;

INSERT INTO shipment_lct (name, capacity)
SELECT name, capacity
FROM temp_shipment_lct
