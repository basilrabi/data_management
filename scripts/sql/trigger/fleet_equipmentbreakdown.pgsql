CREATE OR REPLACE FUNCTION insert_mo_created_on()
RETURNS trigger AS
$BODY$
BEGIN
    IF (NEW.maintenance_order IS NOT NULL) THEN
        UPDATE fleet_equipmentbreakdown
        SET mo_created_on = NOW()
        WHERE id = NEW.id;
    END IF;

    RETURNS NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS fleet_equipmentbreakdown_mo_created_on_insert
ON fleet_equipmentbreakdown;
CREATE TRIGGER fleet_equipmentbreakdown_mo_created_on_insert
AFTER INSERT
ON fleet_equipmentbreakdown
FOR EACH ROW
EXECUTE PROCEDURE insert_mo_created_on();

CREATE OR REPLACE FUNCTION update_mo_created_on()
RETURNS trigger AS
$BODY$
BEGIN
    IF (NEW.maintenance_order IS NULL) THEN
        UPDATE fleet_equipmentbreakdown
        SET mo_created_on = NULL
        WHERE id = NEW.id;
    ELSIF (OLD.maintenance_order IS NULL) THEN
        UPDATE fleet_equipmentbreakdown
        SET mo_created_on = NOW()
        WHERE id = NEW.id;
    ELSIF (OLD.maintenance_order <> NEW.maintenance_order) THEN
        UPDATE fleet_equipmentbreakdown
        SET mo_created_on = NOW()
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS fleet_equipmentbreakdown_mo_created_on_update
ON fleet_equipmentbreakdown;
CREATE TRIGGER fleet_equipmentbreakdown_mo_created_on_update
AFTER UPDATE OF maintenance_order
ON fleet_equipmentbreakdown
FOR EACH ROW
EXECUTE PROCEDURE update_mo_created_on();

