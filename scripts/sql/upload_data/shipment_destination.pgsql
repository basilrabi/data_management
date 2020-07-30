CREATE TEMPORARY TABLE temp_shipment_destination
(
    name character varying(20),
    description text
);

\copy temp_shipment_destination FROM 'data/shipment_destination.csv' DELIMITER ',' CSV;

INSERT INTO shipment_destination (name, description)
SELECT name, description
FROM temp_shipment_destination
