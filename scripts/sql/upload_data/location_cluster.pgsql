CREATE TEMPORARY TABLE temp_location_cluster
(
    name character varying(30),
    z smallint,
    count integer,
    ore_class character varying(1),
    mine_block character varying(20),
    ni double precision,
    fe double precision,
    co double precision,
    distance_from_road double precision,
    road_date date,
    dumping_area text,
    date_scheduled date,
    excavated boolean,
    modified timestamp with time zone,
    geom_text text
);

\copy temp_location_cluster FROM 'data/location_cluster.csv' DELIMITER ',' CSV;

INSERT INTO location_cluster (
    name,
    z,
    count,
    ore_class,
    mine_block,
    ni,
    fe,
    co,
    distance_from_road,
    road_id,
    dumping_area_id,
    date_scheduled,
    excavated,
    modified,
    geom
)
SELECT
    a.name,
    a.z,
    a.count,
    a.ore_class,
    a.mine_block,
    a.ni,
    a.fe,
    a.co,
    a.distance_from_road,
    b.id,
    c.id,
    a.date_scheduled,
    a.excavated,
    a.modified,
    ST_GeomFromEWKT(a.geom_text)
FROM temp_location_cluster a
    LEFT JOIN location_roadarea b
        ON a.road_date = b.date_surveyed
    LEFT JOIN location_stockpile c
        ON a.dumping_area = c.name
