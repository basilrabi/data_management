CREATE TEMPORARY TABLE temp_sampling_drillcoresample
(
    date_received_for_preparation date,
    date_prepared date,
    date_received_for_analysis date,
    date_analyzed date,
    al numeric(6,4),
    al2o3 numeric(6,4),
    arsenic numeric(6,4),
    c numeric(6,4),
    cao numeric(6,4),
    co numeric(6,4),
    cr numeric(6,4),
    cr2o3 numeric(6,4),
    cu numeric(6,4),
    fe numeric(6,4),
    k numeric(6,4),
    mg numeric(6,4),
    mgo numeric(6,4),
    mn numeric(6,4),
    ni numeric(6,4),
    p numeric(6,4),
    pb numeric(6,4),
    s numeric(6,4),
    sc numeric(6,4),
    si numeric(6,4),
    sio2 numeric(6,4),
    zn numeric(6,4),
    ignition_loss numeric(6,4),
    moisture numeric(6,4),
    drillhole character varying(20),
    interval_from numeric(5,3),
    interval_to numeric(5,3),
    lithology character varying(20),
    lithology_modified character varying(20),
    description text,
    excavated_date date
);

\copy temp_sampling_drillcoresample FROM 'data/sampling_drillcoresample.csv' DELIMITER ',' CSV;

INSERT INTO sampling_drillcoresample (
    date_received_for_preparation,
    date_prepared,
    date_received_for_analysis,
    date_analyzed,
    al,
    al2o3,
    arsenic,
    c,
    cao,
    co,
    cr,
    cr2o3,
    cu,
    fe,
    k,
    mg,
    mgo,
    mn,
    ni,
    p,
    pb,
    s,
    sc,
    si,
    sio2,
    zn,
    ignition_loss,
    moisture,
    interval_from,
    interval_to,
    description,
    excavated_date,
    drill_hole_id,
    lithology_id,
    lithology_modified_id
)
SELECT
    core.date_received_for_preparation,
    core.date_prepared,
    core.date_received_for_analysis,
    core.date_analyzed,
    core.al,
    core.al2o3,
    core.arsenic,
    core.c,
    core.cao,
    core.co,
    core.cr,
    core.cr2o3,
    core.cu,
    core.fe,
    core.k,
    core.mg,
    core.mgo,
    core.mn,
    core.ni,
    core.p,
    core.pb,
    core.s,
    core.sc,
    core.si,
    core.sio2,
    core.zn,
    core.ignition_loss,
    core.moisture,
    core.interval_from,
    core.interval_to,
    core.description,
    core.excavated_date,
    dh.id drill_hole_id,
    litho.id lithology_id,
    litho_mod.id lithology_modified_id
FROM temp_sampling_drillcoresample core
    LEFT JOIN location_drillhole dh
        ON dh.name = core.drillhole
    LEFT JOIN sampling_lithology litho
        ON litho.name = core.lithology
    LEFT JOIN sampling_lithology litho_mod
        ON litho_mod.name = core.lithology_modified;
