CREATE TEMPORARY TABLE temp_sampling_shipmentdischargeassay
(
    al numeric(6,4),
    al2o3 numeric(6,4),
    arsenic numeric(6,4),
    c numeric(6,4),
    cao numeric(6,4),
    co numeric(6,4),
    cr numeric(6,4),
    fe numeric(6,4),
    mg numeric(6,4),
    mgo numeric(6,4),
    mn numeric(6,4),
    ni numeric(6,4),
    p numeric(6,4),
    s numeric(6,4),
    sc numeric(6,4),
    si numeric(6,4),
    sio2 numeric(6,4),
    ignition_loss numeric(6,4),
    moisture numeric(6,4),
    wmt numeric(8,3),
    dmt numeric(8,3),
    laboratory_name character varying(20),
    shipment_name character varying(10)
);

\copy temp_sampling_shipmentdischargeassay FROM 'data/sampling_shipmentdischargeassay.csv' DELIMITER ',' CSV;

INSERT INTO sampling_shipmentdischargeassay (
    al,
    al2o3,
    arsenic,
    c,
    cao,
    co,
    cr,
    fe,
    mg,
    mgo,
    mn,
    ni,
    p,
    s,
    sc,
    si,
    sio2,
    ignition_loss,
    moisture,
    wmt,
    dmt,
    laboratory_id,
    shipment_id
)
SELECT
    a.al,
    a.al2o3,
    a.arsenic,
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
    l.id,
    s.id
FROM temp_sampling_shipmentdischargeassay a
    LEFT JOIN sampling_laboratory l
        ON l.name = a.laboratory_name
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
