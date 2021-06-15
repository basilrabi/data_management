CREATE OR REPLACE FUNCTION update_location_anchorage_geometry()
RETURNS trigger AS
$BODY$
/* Whenever the x or y coordinates are updated, the point geometry of
 * anchorage is also updated.
 */
DECLARE
    has_lat_d boolean;
    has_lat_m boolean;
    has_lon_d boolean;
    has_lon_m boolean;
    lat double precision;
    lon double precision;
BEGIN
    SELECT
        NEW.latitude_degree IS NOT NULL,
        NEW.latitude_minutes IS NOT NULL,
        NEW.longitude_degree IS NOT NULL,
        NEW.longitude_minutes IS NOT NULL
    INTO has_lat_d, has_lat_m, has_lon_d, has_lon_m;

    IF (has_lat_d AND has_lat_m AND has_lon_d AND has_lon_m) THEN
        lat := NEW.latitude_degree::double precision + (NEW.latitude_minutes::double precision / 60);
        lon := NEW.longitude_degree::double precision + (NEW.longitude_minutes::double precision / 60);
        UPDATE location_anchorage
        SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_anchorage_geometry_update
ON location_anchorage;
CREATE TRIGGER location_anchorage_geometry_update
AFTER INSERT OR UPDATE OF
latitude_degree,
latitude_minutes,
longitude_degree,
longitude_minutes
ON location_anchorage
FOR EACH ROW EXECUTE PROCEDURE update_location_anchorage_geometry();
