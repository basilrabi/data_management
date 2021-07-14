WITH clipped AS (
    SELECT
        a.id,
        CASE
            WHEN crest.geom IS NULL OR ST_IsEmpty(crest.geom) THEN
                a.geom
            ELSE
                ST_Multi(ST_Intersection(a.geom, crest.geom))
        END geom
    FROM location_cluster a
        LEFT JOIN LATERAL (
            SELECT ST_Union(b.geom) geom
            FROM location_crest b
            WHERE a.z = b.z + 3
                AND ST_Intersects(a.geom, b.geom)
        ) crest ON true
),
block_grade AS (
    SELECT
        clipped.id,
        ST_Area(
            ST_Intersection(
                ST_Expand(ib.geom, 5),
                clipped.geom
            )
        ) area,
        ib.co,
        ib.fe,
        ib.ni
    FROM inventory_block ib, clipped
    WHERE clipped.id = ib.cluster_id
),
area_products AS (
    SELECT
        id,
        SUM(area) total_area,
        SUM(co * area) co_area,
        SUM(fe * area) fe_area,
        SUM(ni * area) ni_area
    FROM block_grade
    GROUP BY id
),
grade_average AS (
    SELECT
        id,
        round((co_area / total_area)::numeric, 2) co,
        round((fe_area / total_area)::numeric, 2) fe,
        round((ni_area / total_area)::numeric, 2) ni
    FROM area_products
)
INSERT INTO location_clippedcluster(
    geom,
    co,
    fe,
    ni,
    ore_class,
    date_scheduled,
    excavated,
    cluster_id,
    latest_layout_date,
    mine_block,
    modified,
    name,
    z
)
SELECT
    clipped.geom,
    grade_average.co,
    grade_average.fe,
    grade_average.ni,
    get_ore_class(grade_average.ni, grade_average.fe) ore_class,
    lc.date_scheduled,
    lc.excavated,
    lc.id,
    lc.latest_layout_date,
    lc.mine_block,
    lc.modified,
    lc.name,
    lc.z
FROM clipped, grade_average, location_cluster lc
WHERE clipped.id = grade_average.id AND grade_average.id = lc.id
