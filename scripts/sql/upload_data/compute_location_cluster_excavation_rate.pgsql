WITH cte_a AS (
    SELECT
        cluster_id,
        CASE
            WHEN depth IS NULL THEN 1
            WHEN depth  > 0 THEN 1
            ELSE 0
        END as assumed_depth
    FROM inventory_block
    WHERE cluster_id IS NOT NULL
),
cte_b AS (
    SELECT
        cluster_id,
        (
            (COUNT(*) - SUM(assumed_depth)) * 100 / COUNT(*)::float8
        )::integer excavation_rate
        FROM cte_a
        GROUP BY cluster_id
)
UPDATE location_cluster
SET excavation_rate = cte_b.excavation_rate
FROM cte_b
WHERE location_cluster.id = cte_b.cluster_id
