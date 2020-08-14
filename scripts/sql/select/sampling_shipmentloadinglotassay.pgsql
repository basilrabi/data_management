SELECT
    a.lot,
    a.ni,
    a.moisture,
    a.wmt,
    c.name shipment
FROM sampling_shipmentloadinglotassay a
    LEFT JOIN sampling_shipmentloadingassay b
        ON b.id = a.shipment_assay_id
    LEFT JOIN shipment_shipment c
        ON c.id = b.shipment_id
    LEFT JOIN shipment_laydaysstatement d
        ON d.shipment_id = c.id
ORDER BY
    d.completed_loading DESC,
    c.name DESC,
    a.lot ASC
