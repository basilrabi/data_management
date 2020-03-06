CREATE OR REPLACE FUNCTION update_location_drillhole_geometry()
RETURNS trigger AS
$BODY$
/* Whenever the x or y coordinates are updated, the point geometry of the
 * drill hole is also updated.
 */
DECLARE
    has_x boolean;
    has_y boolean;
BEGIN
    SELECT NEW.x IS NOT NULL, NEW.y IS NOT NULL
    INTO has_x, has_y;

    IF (has_x AND has_y) THEN
        UPDATE location_drillhole
        SET geom = ST_SetSRID(ST_MakePoint(NEW.x, NEW.y), 3125)
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_drillhole_geometry_update
ON location_drillhole;
CREATE TRIGGER location_drillhole_geometry_update
AFTER INSERT OR UPDATE OF x, y ON location_drillhole
FOR EACH ROW EXECUTE PROCEDURE update_location_drillhole_geometry();
