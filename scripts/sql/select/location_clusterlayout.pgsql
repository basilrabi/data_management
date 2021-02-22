SELECT b.name, a.layout_date
FROM location_clusterlayout a
	LEFT JOIN location_cluster b
		ON a.cluster_id = b.id
ORDER BY
	b.count,
	b.mine_block,
	b.ore_class,
	a.layout_date
