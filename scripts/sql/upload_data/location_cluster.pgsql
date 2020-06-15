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
    date_scheduled date,
    layout_date date,
    excavated boolean,
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
    date_scheduled,
    layout_date,
    excavated,
    geom
)
SELECT
    temp_location_cluster.name,
    temp_location_cluster.z,
    temp_location_cluster.count,
    temp_location_cluster.ore_class,
    temp_location_cluster.mine_block,
    temp_location_cluster.ni,
    temp_location_cluster.fe,
    temp_location_cluster.co,
    temp_location_cluster.distance_from_road,
    location_roadarea.id,
    temp_location_cluster.date_scheduled,
    temp_location_cluster.layout_date,
    temp_location_cluster.excavated,
    ST_GeomFromEWKT(temp_location_cluster.geom_text)
FROM temp_location_cluster
    LEFT JOIN location_roadarea
        ON temp_location_cluster.road_date = location_roadarea.date_surveyed;
