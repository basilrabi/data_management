CREATE TEMPORARY TABLE temp_inventory_block
(
    name character varying(20),
    z smallint,
    ni double precision,
    fe double precision,
    co double precision,
    depth double precision,
    planned_excavation_date date,
    x double precision,
    y double precision
);

\copy temp_inventory_block FROM 'data/inventory_block.csv' DELIMITER ',' CSV;

INSERT INTO inventory_block (
    name,
    z,
    ni,
    fe,
    co,
    depth,
    exposed,
    planned_excavation_date,
    geom
)
SELECT
    name,
    z,
    ni,
    fe,
    co,
    depth,
    depth > 0 and depth <= 3,
    planned_excavation_date,
    ST_SetSRID(ST_MakePoint(x, y), 3125)
FROM temp_inventory_block;
