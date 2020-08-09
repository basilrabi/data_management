SELECT s.name
FROM sampling_approvedshipmentdischargeassay a
    LEFT JOIN sampling_shipmentdischargeassay b
        ON b.id = a.assay_id
    LEFT JOIN shipment_shipment s
        ON s.id = b.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
WHERE a.approved
ORDER BY
    statement.completed_loading DESC,
    s.name DESC
