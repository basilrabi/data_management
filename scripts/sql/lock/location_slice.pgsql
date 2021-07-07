CREATE OR REPLACE FUNCTION lock_location_slice()
RETURNS trigger AS
$BODY$
DECLARE
    intersection_count integer;
BEGIN
    IF (NEW.layer = 2) THEN
        SELECT COUNT(*)
        INTO intersection_count
        FROM location_slice
        WHERE id <> NEW.id
            AND z = NEW.z
            AND layer = 2
            AND ST_Intersects(geom, NEW.geom)
            AND ST_GeometryType(
                ST_Intersection(
                    ST_MakePolygon(ST_Force2D(geom)),
                    ST_MakePolygon(ST_Force2D(NEW.geom))
                )
            ) in ('ST_Polygon', 'ST_MultiPolygon');
        IF (intersection_count > 0) THEN
            RAISE EXCEPTION 'Overlapping crestlines.';
        END IF;
    END IF;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_slice_lock_add
ON location_slice;
CREATE TRIGGER location_slice_lock_add
BEFORE INSERT ON location_slice
FOR EACH ROW
EXECUTE PROCEDURE lock_location_slice();

DROP TRIGGER IF EXISTS location_slice_lock_update
ON location_slice;
CREATE TRIGGER location_slice_lock_update
BEFORE UPDATE OF geom, z ON location_slice
FOR EACH ROW
EXECUTE PROCEDURE lock_location_slice();
