SELECT
    name,
    z,
    ni,
    fe,
    co,
    depth,
    ST_X(geom) x,
    ST_Y(geom) y
FROM inventory_block
ORDER BY name
