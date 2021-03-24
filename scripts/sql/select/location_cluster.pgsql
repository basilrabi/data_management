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
	b.date_surveyed road_date,
	c.name dumping_area,
	a.date_scheduled,
	a.excavated,
	a.modified,
	ST_AsEWKT(a.geom)
FROM location_cluster a
	LEFT JOIN location_roadarea b
		ON a.road_id = b.id
	LEFT JOIN location_stockpile c
		ON a.dumping_area_id = c.id
WHERE a.geom IS NOT NULL
ORDER BY
	a.count,
	a.mine_block,
	a.ore_class
