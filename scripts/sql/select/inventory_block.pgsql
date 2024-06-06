SELECT
    name,
    z,
    density_br,
    density_lim,
    density_sap,
    pp_air,
    pp_br,
    pp_lim,
    pp_sap,
    ni,
    ni_lim,
    ni_sap,
    fe,
    fe_lim,
    fe_sap,
    co,
    co_lim,
    co_sap,
    mg,
    mg_lim,
    mg_sap,
    depth,
    planned_excavation_date,
    ST_X(geom) x,
    ST_Y(geom) y
FROM inventory_block
ORDER BY name

