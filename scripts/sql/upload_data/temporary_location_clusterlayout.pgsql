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
    modified timestamp with time zone,
    geom_text text
);

\copy temp_location_cluster FROM 'data/location_cluster.csv' DELIMITER ',' CSV;

INSERT INTO location_clusterlayout (cluster_id, layout_date)
SELECT b.id, a.layout_date
FROM temp_location_cluster a
    LEFT JOIN location_cluster b
        ON a.name = b.name

WHERE a.layout_date IS NOT NULL;
