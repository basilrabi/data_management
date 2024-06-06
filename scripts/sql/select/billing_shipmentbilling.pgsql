SELECT c.name
FROM billing_shipmentbilling a,
    shipment_laydaysstatement b,
    shipment_shipment c
WHERE a.shipment_id = b.id
    AND b.shipment_id = c.id
ORDER BY b.completed_loading, c.name

