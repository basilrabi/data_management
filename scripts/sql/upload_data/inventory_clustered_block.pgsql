CREATE TEMPORARY TABLE temp_clustered_block
(
    name character varying(20)
);

\copy temp_clustered_block FROM 'data/inventory_clustered_block.csv' DELIMITER ',' CSV;

WITH a AS (
    SELECT
        block_a.name,
        block_b.id,
        block_b.z,
        block_b.geom
    FROM temp_clustered_block block_a
        LEFT JOIN inventory_block block_b
            ON block_a.name = block_b.name
),
b AS (
    SELECT
        a.id AS b_id,
        cluster.id AS c_id
    FROM a
        LEFT JOIN location_cluster cluster
            ON  a.z = cluster.z
                AND (
                    ST_Intersects(a.geom, cluster.geom)
                        OR ST_Overlaps(ST_Expand(a.geom, 5), cluster.geom)
                )

)
UPDATE inventory_block
SET cluster_id = b.c_id
FROM b
WHERE id = b.b_id;
