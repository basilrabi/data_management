CREATE TEMPORARY TABLE temp_shipment_buyer
(
    name character varying(20),
    description text
);

\copy temp_shipment_buyer FROM 'data/shipment_buyer.csv' DELIMITER ',' CSV;

INSERT INTO shipment_buyer (name, description)
SELECT name, description
FROM temp_shipment_buyer
