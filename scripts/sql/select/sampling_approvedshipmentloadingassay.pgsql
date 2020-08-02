SELECT
    a.approved,
    s.name shipment
FROM sampling_approvedshipmentloadingassay a
    LEFT JOIN sampling_shipmentloadingassay b
        ON b.id = a.assay_id
    LEFT JOIN shipment_shipment s
        ON s.id = b.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
ORDER BY statement.completed_loading DESC
