SELECT
	name,
	z,
	ore_class,
	mine_block,
	ni,
	fe,
	co,
	date_scheduled,
	latest_layout_date,
	ST_Area(geom) * 3 as "m³"
FROM location_cluster
WHERE geom IS NOT NULL
	AND NOT excavated
ORDER BY ore_class, count
