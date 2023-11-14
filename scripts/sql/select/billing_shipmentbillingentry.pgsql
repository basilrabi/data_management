SELECT
    a.amount,
    a.last_update,
    a.onboard_handling_amount,
    a.onboard_handling_ton,
    a.tonnage,
    d.name shipment,
    e.name contractor
FROM billing_shipmentbillingentry a,
    billing_shipmentbilling b,
    shipment_laydaysstatement c,
    shipment_shipment d,
    organization_organization e
WHERE a.contractor_id = e.id
    AND a.shipment_id = b.id
    AND b.shipment_id = c.id
    AND c.shipment_id = d.id
ORDER BY
    c.completed_loading,
    d.name,
    e.name
