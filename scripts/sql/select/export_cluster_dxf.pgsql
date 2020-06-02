SELECT
	name AS "Layer",
	date_scheduled AS "Text",
	z - 3 AS "Elevation",
	ST_ExteriorRing((ST_Dump(geom)).geom) AS geom
FROM location_cluster
WHERE geom IS NOT NULL
	AND date_scheduled IS NOT NULL
	AND layout_date IS NULL
