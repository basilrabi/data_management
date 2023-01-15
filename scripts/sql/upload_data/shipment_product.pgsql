CREATE TEMPORARY TABLE temp_shipment_product
(
    name character varying(40),
    description text,
    moisture numeric(6,4),
    ni numeric(6,4),
    fe numeric(6,4)
);

\copy temp_shipment_product FROM 'data/shipment_product.csv' DELIMITER ',' CSV;

INSERT INTO shipment_product (name, description, moisture, ni, fe)
SELECT name, description, moisture, ni, fe
FROM temp_shipment_product
