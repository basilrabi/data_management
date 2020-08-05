CREATE OR REPLACE FUNCTION insert_location_cluster_timestamp()
RETURNS trigger AS
$BODY$
/* Whenever there is no timestamp field in a freshly inserted row, automatically
 * create one.
 */
BEGIN
    NEW.modified = NOW();
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_timestamp_insert
ON location_cluster;
CREATE TRIGGER location_cluster_timestamp_insert
BEFORE INSERT ON location_cluster
FOR EACH ROW
WHEN (NEW.modified IS NULL)
EXECUTE PROCEDURE insert_location_cluster_timestamp();

/* Whenever date_scheduled is modified, update timestamp. */
DROP TRIGGER IF EXISTS location_cluster_timestamp_update
ON location_cluster;
CREATE TRIGGER location_cluster_timestamp_update
BEFORE UPDATE ON location_cluster
FOR EACH ROW
WHEN (
    NEW.date_scheduled <> OLD.date_scheduled OR
    (NEW.date_scheduled IS NOT NULL AND OLD.date_scheduled IS NULL) OR
    (NEW.date_scheduled IS NULL AND OLD.date_scheduled IS NOT NULL)
)
EXECUTE PROCEDURE insert_location_cluster_timestamp();
