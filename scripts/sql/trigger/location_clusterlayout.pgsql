CREATE OR REPLACE FUNCTION delete_location_cluster_layout_date()
RETURNS trigger AS
$BODY$
-- Update location_cluster.latest_layout_date for any deletion in
-- location_clusterlayout.
DECLARE
    new_date date;
BEGIN
    SELECT MAX(layout_date)
    INTO new_date
    FROM location_clusterlayout
    WHERE cluster_id = OLD.cluster_id;

    UPDATE location_cluster
    SET latest_layout_date = new_date
    WHERE id = OLD.cluster_id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_layout_date_delete
ON location_clusterlayout;
CREATE TRIGGER location_cluster_layout_date_delete
AFTER DELETE ON location_clusterlayout
FOR EACH ROW
EXECUTE PROCEDURE delete_location_cluster_layout_date();

CREATE OR REPLACE FUNCTION insert_location_cluster_layout_date()
RETURNS trigger AS
$BODY$
-- Update location_cluster.latest_layout_date for any addition in
-- location_clusterlayout.
DECLARE
    new_date date;
BEGIN
    SELECT MAX(layout_date)
    INTO new_date
    FROM location_clusterlayout
    WHERE cluster_id = NEW.cluster_id;

    UPDATE location_cluster
    SET latest_layout_date = new_date
    WHERE id = NEW.cluster_id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_layout_date_insert
ON location_clusterlayout;
CREATE TRIGGER location_cluster_layout_date_insert
AFTER INSERT ON location_clusterlayout
FOR EACH ROW
EXECUTE PROCEDURE insert_location_cluster_layout_date();

CREATE OR REPLACE FUNCTION update_location_cluster_layout_date()
RETURNS trigger AS
$BODY$
-- Update location_cluster.latest_layout_date for any changes in
-- location_clusterlayout.
DECLARE
    new_date date;
    old_date date;
BEGIN
    SELECT MAX(layout_date)
    INTO new_date
    FROM location_clusterlayout
    WHERE cluster_id = NEW.cluster_id;

    UPDATE location_cluster
    SET latest_layout_date = new_date
    WHERE id = NEW.cluster_id;

    IF (NEW.cluster_id <> OLD.cluster_id) THEN
        SELECT MAX(layout_date)
        INTO old_date
        FROM location_clusterlayout
        WHERE cluster_id = OLD.cluster_id;

        UPDATE location_cluster
        SET latest_layout_date = old_date
        WHERE id = OLD.cluster_id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_layout_date_update
ON location_clusterlayout;
CREATE TRIGGER location_cluster_layout_date_update
AFTER UPDATE ON location_clusterlayout
FOR EACH ROW
EXECUTE PROCEDURE update_location_cluster_layout_date();
