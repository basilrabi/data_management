CREATE TEMPORARY TABLE temp_location_clusterlayout
(
    name character varying(30),
    layout_date date
);

\copy temp_location_clusterlayout FROM 'data/location_clusterlayout.csv' DELIMITER ',' CSV;

INSERT INTO location_clusterlayout (cluster_id, layout_date)
SELECT b.id, a.layout_date
FROM temp_location_clusterlayout a
    LEFT JOIN location_cluster b
        ON a.name = b.name;
