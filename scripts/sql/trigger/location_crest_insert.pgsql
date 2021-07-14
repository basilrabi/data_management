CREATE OR REPLACE FUNCTION insert_location_crest()
RETURNS trigger AS
$BODY$
-- Whenever a crest line is inserted, also insert or update crest.
DECLARE
    crest geometry;
    crest_external geometry;
    crest_valid geometry;
    ring_external geometry;
    ring_external_id bigint;
    ring_internal geometry;
BEGIN
    SELECT geom, id
    INTO ring_external, ring_external_id
    FROM location_slice
    WHERE z = NEW.z
        AND layer = 2
        AND geom && NEW.geom
        AND ST_ContainsProperly(
            ST_MakePolygon(ST_Force2D(geom)),
            ST_MakePolygon(ST_Force2D(NEW.geom))
        );

    IF (ring_external_id IS NULL) THEN
        crest_external := ST_MakePolygon(ST_Force2D(NEW.geom));
        ring_external_id := NEW.id;
    ELSE
        crest_external := ST_MakePolygon(ST_Force2D(ring_external));
    END IF;

    SELECT ST_Union(ST_MakePolygon(ST_Force2D(geom)))
    INTO ring_internal
    FROM location_slice
    WHERE z = NEW.z
        AND layer = 2
        AND geom && crest_external
        AND ST_ContainsProperly(crest_external, geom);

    IF (ring_internal IS NULL OR ST_IsEmpty(ring_internal)) THEN
        crest := ST_MakeValid(crest_external);
    ELSE
        crest := ST_MakeValid(ST_Difference(crest_external, ring_internal));
    END IF;

    IF (ST_GeometryType(crest) = 'ST_GeometryCollection') THEN
        crest_valid := ST_CollectionExtract(crest, 3);
    ELSE
        crest_valid := ST_Multi(crest);
    END IF;

    DELETE FROM location_crest
    WHERE z = NEW.z
        AND (
            ST_Overlaps(geom, crest_external)
                OR ST_Contains(geom, crest_external)
                OR ST_Contains(crest_external, geom)
        );

    INSERT INTO location_crest (slice_id, z, geom)
    VALUES (ring_external_id, NEW.z, crest_valid);

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_crest_insert
ON location_slice;
CREATE TRIGGER location_crest_insert
AFTER INSERT ON location_slice
FOR EACH ROW
WHEN (NEW.layer = 2)
EXECUTE PROCEDURE insert_location_crest();
