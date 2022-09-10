CREATE TEMPORARY TABLE temp_shipment_approvedlaydaysstatement
(
    shipment_name character varying(10),
    approved boolean,
    signed_statement character varying(100)
);

\copy temp_shipment_approvedlaydaysstatement FROM 'data/shipment_approvedlaydaysstatement.csv' DELIMITER ',' CSV;

INSERT INTO shipment_approvedlaydaysstatement (
    approved, signed_statement, statement_id
)
SELECT a.approved, a.signed_statement, b.id
FROM temp_shipment_approvedlaydaysstatement a
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
    LEFT JOIN shipment_laydaysstatement b
        ON b.shipment_id = s.id;

INSERT INTO shipment_approvedlaydaysstatement (approved, statement_id)
SELECT 'f', a.id
FROM shipment_laydaysstatement a
WHERE a.id NOT IN (
    SELECT statement_id
    FROM shipment_approvedlaydaysstatement
)
