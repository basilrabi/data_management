WITH cte_a AS (
    SELECT cluster_id, MAX(layout_date) max_layout_date
    FROM location_clusterlayout
    GROUP BY cluster_id
)
UPDATE location_cluster
SET latest_layout_date = cte_a.max_layout_date
FROM cte_a
WHERE location_cluster.id = cte_a.cluster_id
