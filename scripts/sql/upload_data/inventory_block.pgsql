CREATE TEMPORARY TABLE temp_inventory_block
(
    name character varying(20),
    z smallint,
    ni double precision,
    fe double precision,
    co double precision,
    depth double precision,
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
    geom
)
SELECT
    name,
    z,
    ni,
    fe,
    co,
    depth,
    ST_SetSRID(ST_MakePoint(x, y), 3125)
FROM temp_inventory_block;
