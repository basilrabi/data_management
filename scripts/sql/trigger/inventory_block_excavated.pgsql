CREATE OR REPLACE FUNCTION set_inventory_block_excavated()
RETURNS trigger AS
$BODY$
/* Whenever there a new block is added, the excavated flag is set.
 *
 * TODO: Delete
 * After fully migrating to PG 12, this will not be needed due to generated
 * columns.
 */
BEGIN
    IF (NEW.depth IS NOT NULL) THEN
        UPDATE inventory_block
        SET excavated = CASE
                WHEN NEW.depth > 0 THEN false
                else true
            END
        WHERE id = NEW.id;
    ELSE
        UPDATE inventory_block
        SET excavated = NULL
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS inventory_block_excavated_set
ON inventory_block;
CREATE TRIGGER inventory_block_excavated_set
AFTER INSERT ON inventory_block
FOR EACH ROW
EXECUTE PROCEDURE set_inventory_block_excavated();


/* Whenever there is a change in the depth field of a block, the excavated
 * flag is updated.
 *
 * TODO: Delete
 * After fully migrating to PG 12, this will not be needed due to generated
 * columns.
 */
DROP TRIGGER IF EXISTS inventory_block_excavated_update
ON inventory_block;
CREATE TRIGGER inventory_block_excavated_update
AFTER UPDATE ON inventory_block
FOR EACH ROW
WHEN (NEW.depth <> OLD.depth OR
      (NEW.depth IS NOT NULL AND OLD.depth IS NULL) OR
      (NEW.depth IS NULL AND OLD.cluster_id IS NOT NULL))
EXECUTE PROCEDURE set_inventory_block_excavated();
