SELECT
    a.al,
    a.al2o3,
    a.c,
    a.cao,
    a.co,
    a.cr,
    a.date,
    a.fe,
    a.mg,
    a.mgo,
    a.mn,
    a.ni,
    a.ni_ton,
    a.p,
    a.s,
    a.sc,
    a.si,
    a.sio2,
    a.ignition_loss,
    a.moisture,
    a.wmt,
    a.dmt,
    s.name shipment
FROM sampling_shipmentloadingassay a
    LEFT JOIN shipment_shipment s
        ON s.id = a.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
ORDER BY statement.completed_loading DESC
