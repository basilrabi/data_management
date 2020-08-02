CREATE TEMPORARY TABLE temp_sampling_shipmentloadingassay
(
    al numeric(6,4),
    al2o3 numeric(6,4),
    c numeric(6,4),
    cao numeric(6,4),
    co numeric(6,4),
    cr numeric(6,4),
    date date,
    fe numeric(6,4),
    mg numeric(6,4),
    mgo numeric(6,4),
    mn numeric(6,4),
    ni numeric(6,4),
    ni_ton numeric(7,3),
    p numeric(6,4),
    s numeric(6,4),
    sc numeric(6,4),
    si numeric(6,4),
    sio2 numeric(6,4),
    ignition_loss numeric(6,4),
    moisture numeric(6,4),
    wmt numeric(8,3),
    dmt numeric(8,3),
    shipment_name character varying(10),
    username character varying(150)
);

\copy temp_sampling_shipmentloadingassay FROM 'data/sampling_shipmentloadingassay.csv' DELIMITER ',' CSV;

INSERT INTO sampling_shipmentloadingassay (
    al,
    al2o3,
    c,
    cao,
    co,
    cr,
    date,
    fe,
    mg,
    mgo,
    mn,
    ni,
    ni_ton,
    p,
    s,
    sc,
    si,
    sio2,
    ignition_loss,
    moisture,
    wmt,
    dmt,
    shipment_id,
    chemist_id
)
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
    s.id,
    u.id
FROM temp_sampling_shipmentloadingassay a
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
    LEFT JOIN custom_user u
        ON u.username = a.username
