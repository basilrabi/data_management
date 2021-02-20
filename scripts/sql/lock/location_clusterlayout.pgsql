CREATE OR REPLACE FUNCTION lock_location_clusterlayout_delete()
RETURNS trigger AS
$BODY$
DECLARE
    excavated boolean;
    siblings integer;
BEGIN
    SELECT COUNT(*)
    INTO siblings
    FROM location_clusterlayout
    WHERE cluster_id = OLD.cluster_id;

    SELECT location_cluster.excavated
    INTO excavated
    FROM location_cluster
    WHERE id = OLD.cluster_id;

    IF (siblings < 2 AND excavated) THEN
        RAISE EXCEPTION 'Layout cannot be deleted if cluster is excavated.';
    END IF;

    RETURN OLD;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clusterlayout_lock_delete
ON location_clusterlayout;
CREATE TRIGGER location_clusterlayout_lock_delete
BEFORE DELETE ON location_clusterlayout
FOR EACH ROW
EXECUTE PROCEDURE lock_location_clusterlayout_delete();

CREATE OR REPLACE FUNCTION lock_location_clusterlayout_insert()
RETURNS trigger AS
$BODY$
DECLARE
    latest_date date;
    scheduled_date date;
BEGIN
    SELECT latest_layout_date, date_scheduled
    INTO latest_date, scheduled_date
    FROM location_cluster
    WHERE id = NEW.cluster_id;

    IF (latest_date IS NOT NULL AND NEW.layout_date < latest_date) THEN
        RAISE EXCEPTION 'New layout date cannot be earlier than latest_layout_date.';
    END IF;

    IF (scheduled_date IS NULL) THEN
        RAISE EXCEPTION 'Cannot set layout_date if not yet scheduled by grade control.';
    END IF;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clusterlayout_lock_insert
ON location_clusterlayout;
CREATE TRIGGER location_clusterlayout_lock_insert
BEFORE INSERT ON location_clusterlayout
FOR EACH ROW
EXECUTE PROCEDURE lock_location_clusterlayout_insert();
