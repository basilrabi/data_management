SELECT block.name
FROM inventory_block block
WHERE block.cluster_id IS NOT NULL
ORDER BY block.name
