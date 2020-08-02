CREATE TEMPORARY TABLE temp_shipment_approvedlaydaysstatement
(
    shipment_name character varying(10)
);

\copy temp_shipment_approvedlaydaysstatement FROM 'data/shipment_approvedlaydaysstatement.csv' DELIMITER ',' CSV;

WITH a AS (
    SELECT d.id
    FROM temp_shipment_approvedlaydaysstatement b
        LEFT JOIN shipment_shipment c
            ON c.name = b.shipment_name
        LEFT JOIN shipment_laydaysstatement d
            ON d.shipment_id = c.id
)
UPDATE shipment_approvedlaydaysstatement
SET approved = 't'
FROM a
WHERE statement_id = a.id
