CREATE TEMPORARY TABLE temp_billing_shipmentbillingentry
(
    amount double precision,
    last_update timestamp with time zone,
    onboard_handling_amount double precision,
    onboard_handling_ton double precision,
    tonnage double precision,
    shipment character varying (10),
    contractor character varying (40)
);

\copy temp_billing_shipmentbillingentry FROM 'data/billing_shipmentbillingentry.csv' DELIMITER ',' CSV;

INSERT INTO billing_shipmentbillingentry (
    amount,
    contractor_id,
    last_update,
    onboard_handling_amount,
    onboard_handling_ton,
    shipment_id,
    tonnage
)
SELECT
    a.amount,
    b.id,
    a.last_update,
    a.onboard_handling_amount,
    a.onboard_handling_ton,
    e.id,
    a.tonnage
FROM temp_billing_shipmentbillingentry a
    LEFT JOIN organization_organization b
        ON a.contractor = b.name
    LEFT JOIN shipment_shipment c
        ON a.shipment = c.name
    LEFT JOIN shipment_laydaysstatement d
        ON c.id = d.shipment_id
    LEFT JOIN billing_shipmentbilling e
        ON d.id = e.shipment_id

