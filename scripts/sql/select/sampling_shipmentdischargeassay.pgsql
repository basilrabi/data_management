SELECT
    a.al,
    a.al2o3,
    a.c,
    a.cao,
    a.co,
    a.cr,
    a.fe,
    a.mg,
    a.mgo,
    a.mn,
    a.ni,
    a.p,
    a.s,
    a.sc,
    a.si,
    a.sio2,
    a.ignition_loss,
    a.moisture,
    a.wmt,
    a.dmt,
    l.name laboratory,
    s.name shipment
FROM sampling_shipmentdischargeassay a
    LEFT JOIN sampling_laboratory l
        ON l.id = a.laboratory_id
    LEFT JOIN shipment_shipment s
        ON s.id = a.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
ORDER BY
    statement.completed_loading,
    s.name
