CREATE OR REPLACE FUNCTION set_inventory_block_exposed()
RETURNS trigger AS
$BODY$
/* Whenever there a new block is added, the exposed flag is set.
 *
 * TODO: Delete when Django supports generated columns
 */
BEGIN
    IF (NEW.depth IS NOT NULL) THEN
        NEW.exposed = NEW.depth > 0 and NEW.depth <= 3;
    ELSE
        NEW.exposed = NULL;
    END IF;

    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS inventory_block_exposed_set
ON inventory_block;
CREATE TRIGGER inventory_block_exposed_set
BEFORE INSERT ON inventory_block
FOR EACH ROW
EXECUTE PROCEDURE set_inventory_block_exposed();


-- Whenever there is a change in the depth field of a block, the exposed
-- flag is updated.
DROP TRIGGER IF EXISTS inventory_block_exposed_update
ON inventory_block;
CREATE TRIGGER inventory_block_exposed_update
BEFORE UPDATE ON inventory_block
FOR EACH ROW
WHEN (NEW.depth <> OLD.depth OR
      (NEW.depth IS NOT NULL AND OLD.depth IS NULL) OR
      (NEW.depth IS NULL AND OLD.cluster_id IS NOT NULL))
EXECUTE PROCEDURE set_inventory_block_exposed();
