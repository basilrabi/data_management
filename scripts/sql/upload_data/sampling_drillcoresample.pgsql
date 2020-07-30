CREATE TEMPORARY TABLE temp_sampling_drillcoresample
(
    date_received_for_preparation date,
    date_prepared date,
    date_received_for_analysis date,
    date_analyzed date,
    al numeric(6,4),
    c numeric(6,4),
    co numeric(6,4),
    cr numeric(6,4),
    fe numeric(6,4),
    mg numeric(6,4),
    ni numeric(6,4),
    sc numeric(6,4),
    si numeric(6,4),
    moisture numeric(6,4),
    drillhole character varying(20),
    interval_from numeric(5,3),
    interval_to numeric(5,3),
    lithology character varying(10),
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
    c,
    co,
    cr,
    fe,
    mg,
    ni,
    sc,
    si,
    moisture,
    interval_from,
    interval_to,
    description,
    excavated_date,
    drill_hole_id,
    lithology_id
)
SELECT
    core.date_received_for_preparation,
    core.date_prepared,
    core.date_received_for_analysis,
    core.date_analyzed,
    core.al,
    core.c,
    core.co,
    core.cr,
    core.fe,
    core.mg,
    core.ni,
    core.sc,
    core.si,
    core.moisture,
    core.interval_from,
    core.interval_to,
    core.description,
    core.excavated_date,
    dh.id drill_hole_id,
    litho.id lithology_id
FROM temp_sampling_drillcoresample core
    LEFT JOIN location_drillhole dh
        ON dh.name = core.drillhole
    LEFT JOIN sampling_lithology litho
        ON litho.name = core.lithology;
