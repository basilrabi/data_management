CREATE OR REPLACE FUNCTION lock_location_cluster_date_scheduled()
RETURNS trigger AS
$BODY$
BEGIN
    IF (OLD.layout_date IS NOT NULL) THEN
        RAISE EXCEPTION
            'date_scheduled cannot be modified if layout_date is set.';
    END IF;

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

    IF (OLD.excavated) THEN
        RAISE EXCEPTION
            'Cluster is already excavated. Cannot modify.';
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

CREATE OR REPLACE FUNCTION lock_location_cluster_layout_date()
RETURNS trigger AS
$BODY$
BEGIN
    IF (OLD.excavated AND NEW.layout_date IS NULL) THEN
        RAISE EXCEPTION
            'Cluster is already excavated. Cannot set to NULL';
    END IF;

    IF (OLD.date_scheduled IS NULL AND NEW.layout_date IS NOT NULL) THEN
        RAISE EXCEPTION
            'Cannot set layout_date if net yet scheduled by grade control.';
    END IF;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_layout_date_lock
ON location_cluster;
CREATE TRIGGER location_cluster_layout_date_lock
BEFORE UPDATE OF layout_date ON location_cluster
FOR EACH ROW
WHEN (NEW.layout_date <> OLD.layout_date OR
      (NEW.layout_date IS NULL AND OLD.layout_date IS NOT NULL) OR
      (NEW.layout_date IS NOT NULL AND OLD.layout_date IS NULL))
EXECUTE PROCEDURE lock_location_cluster_layout_date();
