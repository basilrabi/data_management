CREATE OR REPLACE FUNCTION lock_locationslice_add_due_to_geom()
RETURNS trigger AS
$BODY$
DECLARE
    intersection_count integer;
BEGIN
    IF (NEW.layer = 2 AND ST_IsClosed(NEW.geom)) THEN
        SELECT COUNT(*)
        INTO intersection_count
        FROM location_slice
        WHERE id <> NEW.id
            AND z = NEW.z
            AND layer = 2
            AND ST_Intersects(
                ST_MakePolygon(ST_Force2D(geom)),
                ST_MakePolygon(ST_Force2D(NEW.geom))
            )
            AND ST_GeometryType(
                ST_Intersection(
                    ST_MakePolygon(ST_Force2D(geom)),
                    ST_MakePolygon(ST_Force2D(NEW.geom))
                )
            ) in ('ST_Polygon', 'ST_MultiPolygon')
            AND NOT ST_IsEmpty(
                ST_Intersection(
                    ST_Force2D(geom), ST_Force2D(NEW.geom)
                )
            );
        IF (intersection_count > 0) THEN
            RAISE EXCEPTION 'Overlapping crestlines.';
        END IF;

        WITH ring_counts AS (
            SELECT a.id, COUNT(lat_a.id) ring_count
            FROM location_slice a
                LEFT JOIN LATERAL (
                    SELECT b.id
                    FROM location_slice b
                    WHERE a.id <> b.id
                        AND b.z = a.z
                        AND b.layer = a.layer
                        AND b.geom && a.geom
                        AND ST_ContainsProperly(
                            ST_MakePolygon(ST_Force2D(b.geom)),
                            ST_MakePolygon(ST_Force2D(a.geom))
                        )
                ) lat_a on true
            WHERE a.z = NEW.z
                AND a.layer = 2
                AND a.geom && NEW.geom
            GROUP BY a.id
        )
        SELECT max(ring_count)
        INTO intersection_count
        FROM ring_counts;

        IF (intersection_count > 1) THEN
            RAISE EXCEPTION '3rd level internal rings not allowed.';
        END IF;
    END IF;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_slice_lock_add
ON location_slice;
CREATE TRIGGER location_slice_lock_add
AFTER INSERT ON location_slice
FOR EACH ROW
EXECUTE PROCEDURE lock_locationslice_add_due_to_geom();

CREATE OR REPLACE FUNCTION lock_locationslice_delete_due_to_layout()
RETURNS trigger AS
$BODY$
DECLARE
    intersection_count integer;
BEGIN
    IF (OLD.layer = 2) THEN
        WITH crest_boundary AS (
            SELECT a.id, ST_Union(boundary.geom) geom
            FROM location_crest a
                LEFT JOIN LATERAL (
                    SELECT (ST_Dump(b.geom)).geom
                    FROM location_crest b
                        WHERE a.id = b.id
                ) boundary ON true
            WHERE a.z = OLD.z
                AND a.geom && OLD.geom
            GROUP BY a.id
        )
        SELECT COUNT(*)
        INTO intersection_count
        FROM location_crest a, location_clippedcluster b, crest_boundary c
        WHERE a.id = c.id
            AND a.z + 3 = b.z
            AND ST_Contains(
                c.geom,
                ST_MakePolygon(ST_Force2D(OLD.geom))
            )
            AND ST_Contains(c.geom, b.geom)
            AND b.latest_layout_date IS NOT NULL;

        IF (intersection_count > 0) THEN
            RAISE EXCEPTION 'Affected cluster with layout exists.';
        END IF;
    END IF;

    RETURN OLD;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_slice_lock_delete
ON location_slice;
CREATE TRIGGER location_slice_lock_delete
BEFORE DELETE ON location_slice
FOR EACH ROW
EXECUTE PROCEDURE lock_locationslice_delete_due_to_layout();
