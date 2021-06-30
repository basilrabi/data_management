CREATE TEMPORARY TABLE temp_location_anchorage
(
    name character varying(10),
    anchored timestamp with time zone,
    latitude_degree smallint,
    latitude_minutes numeric(7,5),
    longitude_degree smallint,
    longitude_minutes numeric(7,5)
);

\copy temp_location_anchorage FROM 'data/location_anchorage.csv' DELIMITER ',' CSV;

INSERT INTO location_anchorage (
    anchored,
    latitude_degree,
    latitude_minutes,
    longitude_degree,
    longitude_minutes,
    geom,
    laydays_id
)
SELECT
    a.anchored,
    a.latitude_degree,
    a.latitude_minutes,
    a.longitude_degree,
    a.longitude_minutes,
    ST_SetSRID(ST_MakePoint(
        a.longitude_degree::double precision + (a.longitude_minutes::double precision / 60),
        a.latitude_degree::double precision + (a.latitude_minutes::double precision / 60)
    ), 4326),
    c.id
FROM temp_location_anchorage a
    LEFT JOIN shipment_shipment b
        ON a.name = b.name
    LEFT JOIN shipment_laydaysstatement c
        ON b.id = c.shipment_id;
