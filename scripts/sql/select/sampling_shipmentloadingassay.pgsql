SELECT
    a.al,
    a.al2o3,
    a.arsenic,
    a.c,
    a.cao,
    a.co,
    a.cr,
    a.cr2o3,
    a.cu,
    a.date,
    a.fe,
    a.k,
    a.mg,
    a.mgo,
    a.mn,
    a.ni,
    a.ni_ton,
    a.p,
    a.pb,
    a.s,
    a.sc,
    a.si,
    a.sio2,
    a.zn,
    a.ignition_loss,
    a.moisture,
    a.wmt,
    a.dmt,
    s.name shipment,
    u.username
FROM sampling_shipmentloadingassay a
    LEFT JOIN shipment_shipment s
        ON s.id = a.shipment_id
    LEFT JOIN shipment_laydaysstatement statement
        ON statement.shipment_id = s.id
    LEFT JOIN custom_user u
        ON u.id = a.chemist_id
ORDER BY
    statement.completed_loading DESC,
    s.name DESC
