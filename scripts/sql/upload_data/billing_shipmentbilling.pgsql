CREATE TEMPORARY TABLE temp_billing_shipmentbilling
(
    shipment character varying(10)
);

\copy temp_billing_shipmentbilling FROM 'data/billing_shipmentbilling.csv' DELIMITER ',' CSV;

INSERT INTO billing_shipmentbilling (
    shipment_id
)
SELECT c.id
FROM temp_billing_shipmentbilling a,
    shipment_shipment b,
    shipment_laydaysstatement c
WHERE a.shipment = b.name
    AND b.id = c.shipment_id

