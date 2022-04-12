SELECT
    s.name,
    a.approved,
    a.certificate
FROM sampling_approvedshipmentdischargeassay a
    LEFT JOIN sampling_shipmentdischargeassay b
        ON b.id = a.assay_id
    LEFT JOIN shipment_shipment s
        ON s.id = b.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
WHERE a.approved OR a.certificate IS NOT NULL
ORDER BY
    statement.completed_loading DESC,
    s.name DESC
