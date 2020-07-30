CREATE TEMPORARY TABLE temp_location_drillhole
(
    name character varying(20),
    date_drilled date,
    local_block character varying(20),
    local_easting character varying(20),
    local_northing character varying(20),
    local_z double precision,
    x double precision,
    y double precision,
    z double precision,
    z_present double precision
);

\copy temp_location_drillhole FROM 'data/location_drillhole.csv' DELIMITER ',' CSV;

INSERT INTO location_drillhole (
    name,
    date_drilled,
    local_block,
    local_easting,
    local_northing,
    local_z,
    x,
    y,
    z,
    z_present
)
SELECT
    name,
    date_drilled,
    local_block,
    local_easting,
    local_northing,
    local_z,
    x,
    y,
    z,
    z_present
FROM temp_location_drillhole;
