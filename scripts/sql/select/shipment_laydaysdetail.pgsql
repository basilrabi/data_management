SELECT
    shipment_shipment.name,
    shipment_laydaysdetail.interval_from,
    shipment_laydaysdetail.laytime_rate,
    shipment_laydaysdetail.interval_class,
    shipment_laydaysdetail.remarks
FROM shipment_laydaysdetail
    LEFT JOIN shipment_laydaysstatement
        ON shipment_laydaysdetail.laydays_id = shipment_laydaysstatement.id
    LEFT JOIN shipment_shipment
        ON shipment_laydaysstatement.shipment_id = shipment_shipment.id
ORDER BY
    shipment_laydaysstatement.completed_loading,
    shipment_shipment.name,
    shipment_laydaysdetail.interval_from
