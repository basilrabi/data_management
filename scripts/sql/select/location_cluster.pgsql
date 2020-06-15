SELECT
	name,
	z,
	count,
	ore_class,
	mine_block,
	ni,
	fe,
	co,
	distance_from_road,
	location_roadarea.date_surveyed road_date,
	date_scheduled,
	layout_date,
	excavated,
	ST_AsEWKT(location_cluster.geom)
FROM location_cluster
	LEFT JOIN location_roadarea
		ON location_cluster.road_id = location_roadarea.id
WHERE location_cluster.geom IS NOT NULL
ORDER BY
	location_cluster.count,
	location_cluster.mine_block,
	location_cluster.ore_class
