CREATE OR REPLACE FUNCTION update_location_crest()
RETURNS trigger AS
$BODY$
-- Whenever a crest line is deleted, also update crest.
DECLARE
    crest geometry;
    crest_valid geometry;
    ring_external geometry;
    ring_internal geometry;
BEGIN
    WITH crest_boundary AS (
        SELECT a.id, ST_Union(ST_MakePolygon(boundary.geom)) geom
        FROM location_crest a
            LEFT JOIN LATERAL (
                SELECT (ST_Dump(ST_Boundary(b.geom))).geom
                FROM location_crest b
                    WHERE a.id = b.id
            ) boundary ON true
        WHERE a.z = OLD.z
            AND a.geom && OLD.geom
        GROUP BY a.id
    )
    SELECT geom
    INTO ring_external
    FROM crest_boundary
    WHERE ST_Contains(geom, ST_MakePolygon(ST_Force2D(OLD.geom)));

    IF (ST_Equals(ring_external, ST_MakePolygon(ST_Force2D(OLD.geom)))) THEN
        DELETE FROM location_crest
        WHERE z = OLD.z
            AND ST_Contains(ring_external, geom);

        WITH raw_crest AS (
            SELECT
                id,
                z,
                ST_MakeValid(ST_MakePolygon(ST_Force2D(geom))) geom
            FROM location_slice
            WHERE layer = 2
                AND z = OLD.z
                AND geom && ring_external
                AND ST_ContainsProperly(
                    ring_external,
                    ST_MakePolygon(ST_Force2D(geom))
                )
        )
        INSERT INTO location_crest (slice_id, z, geom)
        SELECT
            id,
            z,
            CASE
                WHEN (ST_GeometryType(geom) = 'ST_GeometryCollection') THEN
                    ST_CollectionExtract(geom, 3)
                ELSE
                    ST_Multi(geom)
            END
        FROM raw_crest;
    ELSE
        SELECT ST_Union(ST_MakePolygon(ST_Force2D(geom)))
        INTO ring_internal
        FROM location_slice
        WHERE z = OLD.z
            AND layer = 2
            AND geom && ring_external
            AND ST_ContainsProperly(
                ring_external,
                ST_MakePolygon(ST_Force2D(geom))
            );

        IF (ring_internal IS NULL OR ST_IsEmpty(ring_internal)) THEN
            crest := ST_MakeValid(ring_external);
        ELSE
            crest := ST_MakeValid(ST_Difference(ring_external, ring_internal));
        END IF;

        IF (ST_GeometryType(crest) = 'ST_GeometryCollection') THEN
            crest_valid := ST_CollectionExtract(crest, 3);
        ELSE
            crest_valid := ST_Multi(crest);
        END IF;

        UPDATE location_crest
        SET geom = crest_valid
        WHERE z = OLD.z
            AND (
                ST_Overlaps(geom, crest_valid)
                    OR ST_Contains(geom, crest_valid)
                    OR ST_Contains(crest_valid, geom)
            );
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_crest_update
ON location_slice;
CREATE TRIGGER location_crest_update
AFTER DELETE ON location_slice
FOR EACH ROW
WHEN (OLD.layer = 2)
EXECUTE PROCEDURE update_location_crest();
