SELECT
    s.name,
    a.approved,
    a.certificate,
    a.mgb_receipt
FROM sampling_approvedshipmentloadingassay a
    LEFT JOIN sampling_shipmentloadingassay b
        ON b.id = a.assay_id
    LEFT JOIN shipment_shipment s
        ON s.id = b.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
WHERE a.approved OR
    a.certificate IS NOT NULL OR
    a.mgb_receipt IS NOT NULL
ORDER BY
    statement.completed_loading DESC,
    s.name DESC
