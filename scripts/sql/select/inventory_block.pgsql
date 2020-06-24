SELECT
    name,
    z,
    ni,
    fe,
    co,
    depth,
    planned_excavation_date,
    ST_X(geom) x,
    ST_Y(geom) y
FROM inventory_block
ORDER BY name
