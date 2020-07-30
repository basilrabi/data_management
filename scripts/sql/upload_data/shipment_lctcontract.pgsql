CREATE TEMPORARY TABLE temp_shipment_lctcontract
(
    name character varying(50),
    start date,
    "end" date
);

\copy temp_shipment_lctcontract FROM 'data/shipment_lctcontract.csv' DELIMITER ',' CSV;


INSERT INTO shipment_lctcontract (start, "end", lct_id)
SELECT a.start, a."end", b.id
FROM temp_shipment_lctcontract a
    LEFT JOIN shipment_lct b
        ON a.name = b.name
