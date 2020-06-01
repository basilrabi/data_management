SELECT
	name AS "Layer",
	date_scheduled AS "Text",
	z - 3 AS "Elevation",
	ST_Translate(ST_Force3D(geom), 0, 0, z - 3) AS geom
FROM location_cluster
WHERE geom IS NOT NULL
	AND date_scheduled IS NOT NULL
	AND layout_date IS NULL
