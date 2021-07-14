WITH rings AS (
    SELECT a.id, a.geom, a.z, outside_ring.nrings
    FROM location_slice a
        LEFT JOIN LATERAL (
            SELECT COUNT(b.id) nrings
            FROM location_slice b
            WHERE b.id <> a.id
                AND b.layer = 2
                AND b.z = a.z
                AND b.geom && a.geom
                AND ST_ContainsProperly(
                    ST_MakePolygon(ST_Force2D(b.geom)),
                    ST_MakePolygon(ST_Force2D(a.geom))
                )
        ) outside_ring ON true
    WHERE a.layer = 2
),
crest AS (
    SELECT
        a.id,
        a.z,
        CASE
            WHEN ring_internal.geom IS NULL OR ST_IsEmpty(ring_internal.geom) THEN
                ST_MakeValid(ST_Multi(ST_MakePolygon(ST_Force2D(a.geom))))
            ELSE
                ST_Multi(
                    ST_MakeValid(
                        ST_Difference(
                            ST_Multi(ST_MakePolygon(ST_Force2D(a.geom))),
                            ring_internal.geom
                        )
                    )
                )
        END geom
    FROM rings a
        LEFT JOIN LATERAL (
            SELECT ST_Union(ST_MakePolygon(ST_Force2D(b.geom))) geom
            FROM location_slice b
            WHERE b.id <> a.id
                AND b.layer = 2
                AND b.z = a.z
                AND b.geom && a.geom
                AND ST_ContainsProperly(
                    ST_MakePolygon(ST_Force2D(a.geom)),
                    ST_MakePolygon(ST_Force2D(b.geom))
                )
        ) ring_internal ON true
    WHERE a.nrings = 0
)
INSERT INTO location_crest (slice_id, z, geom)
SELECT
    id,
    z,
    CASE
        WHEN ST_GeometryType(geom) = 'ST_GeometryCollection' THEN
            ST_CollectionExtract(geom, 3)
        ELSE
            geom
    END geom
FROM crest
