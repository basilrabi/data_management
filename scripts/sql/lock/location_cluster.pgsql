CREATE OR REPLACE FUNCTION lock_location_cluster_date_scheduled()
RETURNS trigger AS
$BODY$
BEGIN
    IF (OLD.geom IS NULL AND NEW.date_scheduled IS NOT NULL) THEN
        RAISE EXCEPTION
            'Cannot set date if geometry is null.';
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_date_scheduled_lock
ON location_cluster;
CREATE TRIGGER location_cluster_date_scheduled_lock
BEFORE UPDATE OF date_scheduled ON location_cluster
FOR EACH ROW
WHEN (NEW.date_scheduled <> OLD.date_scheduled OR
      (NEW.date_scheduled IS NULL AND OLD.date_scheduled IS NOT NULL) OR
      (NEW.date_scheduled IS NOT NULL AND OLD.date_scheduled IS NULL))
EXECUTE PROCEDURE lock_location_cluster_date_scheduled();

CREATE OR REPLACE FUNCTION lock_location_cluster_geometry()
RETURNS trigger AS
$BODY$
BEGIN
    IF (OLD.date_scheduled IS NOT NULL) THEN
        RAISE EXCEPTION 'Geometry cannot be modified if date_scheduled is set.';
    END IF;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_geometry_lock
ON location_cluster;
CREATE TRIGGER location_cluster_geometry_lock
BEFORE UPDATE OF geom ON location_cluster
FOR EACH ROW
WHEN (ST_AsText(NEW.geom) <> ST_AsText(OLD.geom) OR
      (NEW.geom IS NULL AND OLD.geom IS NOT NULL))
EXECUTE PROCEDURE lock_location_cluster_geometry();
