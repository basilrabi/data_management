CREATE OR REPLACE FUNCTION refresh_trip_validity_after_laydays_change()
RETURNS trigger AS
$BODY$
-- Whenever the laydays statement is updated, also update the validity of the
-- LCT trip.
DECLARE
    new_vessel_id integer;
    old_vessel_id integer;
BEGIN
    SELECT vessel_id
    INTO new_vessel_id
    FROM shipment_shipment
    WHERE id = NEW.shipment_id;

    SELECT vessel_id
    INTO old_vessel_id
    FROM shipment_shipment
    WHERE id = OLD.shipment_id;

    IF OLD.commenced_loading IS NOT NULL
        AND OLD.completed_loading IS NOT NULL
        AND old_vessel_id IS NOT NULL THEN

        UPDATE shipment_trip
        SET valid = false
        WHERE vessel_id = old_vessel_id
            AND (
                interval_to >= OLD.commenced_loading
                    OR interval_to IS NULL
            )
            AND interval_from <= OLD.completed_loading
            AND valid;

    END IF;

    IF NEW.commenced_loading IS NOT NULL
        AND NEW.completed_loading IS NOT NULL
        AND new_vessel_id IS NOT NULL THEN

        UPDATE shipment_trip
        SET valid = true
        WHERE vessel_id = new_vessel_id
            AND (
                interval_to >= NEW.commenced_loading
                    OR interval_to IS NULL
            )
            AND interval_from <= NEW.completed_loading
            AND NOT valid;

    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trip_validity_update_after_laydays_change
ON shipment_laydaysstatement;

CREATE TRIGGER trip_validity_update_after_laydays_change
AFTER INSERT OR UPDATE OF commenced_loading, completed_loading
ON shipment_laydaysstatement
FOR EACH ROW
EXECUTE PROCEDURE refresh_trip_validity_after_laydays_change();

CREATE OR REPLACE FUNCTION refresh_trip_validity_after_shipment_change()
RETURNS trigger AS
$BODY$
-- Whenever the shipment vessel is updated, also update the validity of the
-- LCT trip.
DECLARE
    loading_commenced timestamp with time zone;
    loading_completed timestamp with time zone;
BEGIN
    SELECT commenced_loading
    INTO loading_commenced
    FROM shipment_laydaysstatement
    WHERE shipment_id = NEW.id;

    SELECT completed_loading
    INTO loading_completed
    FROM shipment_laydaysstatement
    WHERE shipment_id = NEW.id;

    IF loading_commenced IS NOT NULL AND loading_completed IS NOT NULL THEN

        -- null to non-null
        IF OLD.vessel_id IS NULL AND NEW.vessel_id IS NOT NULL THEN

            UPDATE shipment_trip
            SET valid = true
            WHERE vessel_id = NEW.vessel_id
                AND (
                    interval_to >= loading_commenced
                        OR interval_to IS NULL
                )
                AND interval_from <= loading_completed
                AND NOT valid;

        -- non-null to null
        ELSIF OLD.vessel_id IS NOT NULL THEN

            UPDATE shipment_trip
            SET valid = false
            WHERE vessel_id = OLD.vessel_id
                AND (
                    interval_to >= loading_commenced
                        OR interval_to IS NULL
                )
                AND interval_from <= loading_completed
                AND valid;

        -- update
            IF OLD.vessel_id <> NEW.vessel_id THEN

                UPDATE shipment_trip
                SET valid = true
                WHERE vessel_id = NEW.vessel_id
                    AND (
                        interval_to >= loading_commenced
                            OR interval_to IS NULL
                    )
                    AND interval_from <= loading_completed
                    AND NOT valid;

            END IF;

        END IF;

    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trip_validity_update_after_shipment_change
ON shipment_shipment;
CREATE TRIGGER trip_validity_update_after_shipment_change
AFTER INSERT OR UPDATE OF vessel_id
ON shipment_shipment
FOR EACH ROW
EXECUTE PROCEDURE refresh_trip_validity_after_shipment_change();

CREATE OR REPLACE FUNCTION refresh_shipment_trip_after_trip_change()
RETURNS trigger AS
$BODY$
-- Whenever there are any changes on shipment_trip intervals, validy and
-- continuity are updated.
BEGIN
    IF (NEW IS NULL OR OLD.lct_id <> NEW.lct_id) THEN
        -- If a trip is deleted or lct is replaced, update adjacent trips
        WITH trip_previous AS (
            SELECT id
            FROM shipment_trip
            WHERE lct_id = OLD.lct_id
                AND id <> OLD.id
                AND interval_from < OLD.interval_from
            ORDER BY interval_from DESC
            LIMIT 1
        ),
        trip_next AS (
            SELECT id
            FROM shipment_trip
            WHERE lct_id = OLD.lct_id
                AND interval_from > OLD.interval_from
            ORDER BY interval_from ASC
            LIMIT 1
        ), cte_a AS (
            SELECT * FROM trip_previous
            UNION
            SELECT * FROM trip_next
        ),
        cte_b AS (
            SELECT
                shipment_trip.id,
                shipment_set.shipment_set > 0 AS valid,
                CASE
                    WHEN shipment_trip.interval_to IS NULL THEN false
                    WHEN shipment_trip.interval_from <> previous_trip.interval_to THEN false
                    WHEN shipment_trip.interval_to <> next_trip.interval_from THEN false
                    ELSE true
                END continuous
            FROM shipment_trip
            LEFT JOIN LATERAL (
                SELECT COUNT(*) shipment_set
                FROM shipment_shipment
                LEFT JOIN shipment_laydaysstatement
                    ON shipment_shipment.id = shipment_laydaysstatement.shipment_id
                WHERE shipment_shipment.vessel_id = shipment_trip.vessel_id
                    AND shipment_laydaysstatement.commenced_loading <= shipment_trip.interval_to
                    AND (
                        shipment_laydaysstatement.completed_loading IS NULL
                            OR shipment_laydaysstatement.commenced_loading >= shipment_trip.interval_to
                    )
            ) shipment_set ON true
            LEFT JOIN LATERAL (
                SELECT interval_to
                FROM shipment_trip ljl
                WHERE ljl.id <> shipment_trip.id
                    AND ljl.lct_id = shipment_trip.lct_id
                    AND ljl.interval_from < shipment_trip.interval_from
                ORDER BY interval_from DESC
                LIMIT 1
            ) previous_trip ON true
            LEFT JOIN LATERAL (
                SELECT interval_from
                FROM shipment_trip ljl
                WHERE ljl.id <> shipment_trip.id
                    AND ljl.lct_id = shipment_trip.lct_id
                    AND ljl.interval_from > shipment_trip.interval_from
                ORDER BY interval_from ASC
                LIMIT 1
            ) next_trip ON true
            WHERE shipment_trip.id IN (SELECT id FROM cte_a)
        )
        UPDATE shipment_trip
        SET valid = cte_b.valid,
            continuous = cte_b.continuous
        FROM cte_b
        WHERE shipment_trip.id = cte_b.id;
    END IF;

    IF NEW IS NOT NULL THEN
        WITH trip_previous AS (
            SELECT id
            FROM shipment_trip
            WHERE lct_id = NEW.lct_id
                AND id <> NEW.id
                AND interval_from < NEW.interval_from
            ORDER BY interval_from DESC
            LIMIT 1
        ), trip_next AS (
            SELECT id
            FROM shipment_trip
            WHERE lct_id = NEW.lct_id
                AND interval_from > NEW.interval_from
            ORDER BY interval_from ASC
            LIMIT 1
        ),
        cte_a AS (
            SELECT id FROM trip_previous
            UNION
            SELECT id FROM trip_next
        ),
        cte_b AS (
            SELECT
                shipment_trip.id,
                shipment_set.shipment_set > 0 AS valid,
                CASE
                    WHEN shipment_trip.interval_to IS NULL THEN false
                    WHEN shipment_trip.interval_from <> previous_trip.interval_to THEN false
                    WHEN shipment_trip.interval_to <> next_trip.interval_from THEN false
                    ELSE true
                END continuous
            FROM shipment_trip
            LEFT JOIN LATERAL (
                SELECT COUNT(*) shipment_set
                FROM shipment_shipment
                LEFT JOIN shipment_laydaysstatement
                    ON shipment_shipment.id = shipment_laydaysstatement.shipment_id
                WHERE shipment_shipment.vessel_id = shipment_trip.vessel_id
                    AND shipment_laydaysstatement.commenced_loading <= shipment_trip.interval_to
                    AND (
                        shipment_laydaysstatement.completed_loading IS NULL
                            OR shipment_laydaysstatement.completed_loading >= shipment_trip.interval_from
                    )
            ) shipment_set ON true
            LEFT JOIN LATERAL (
                SELECT interval_to
                FROM shipment_trip ljl
                WHERE ljl.id <> shipment_trip.id
                    AND ljl.lct_id = shipment_trip.lct_id
                    AND ljl.interval_from < shipment_trip.interval_from
                ORDER BY interval_from DESC
                LIMIT 1
            ) previous_trip ON true
            LEFT JOIN LATERAL (
                SELECT interval_from
                FROM shipment_trip ljl
                WHERE ljl.id <> shipment_trip.id
                    AND ljl.lct_id = shipment_trip.lct_id
                    AND ljl.interval_from > shipment_trip.interval_from
                ORDER BY interval_from ASC
                LIMIT 1
            ) next_trip ON true
            WHERE shipment_trip.id IN (SELECT id FROM cte_a)
                OR shipment_trip.id = NEW.id
        )
        UPDATE shipment_trip
        SET valid = cte_b.valid,
            continuous = cte_b.continuous
        FROM cte_b
        WHERE shipment_trip.id = cte_b.id;
    END IF;


    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trip_refresh_after_trip_update
ON shipment_trip;
CREATE TRIGGER trip_refresh_after_trip_update
AFTER DELETE OR UPDATE OF interval_from, interval_to, lct_id, vessel_id
ON shipment_trip
FOR EACH ROW EXECUTE PROCEDURE refresh_shipment_trip_after_trip_change();

CREATE OR REPLACE FUNCTION refresh_shipment_trip_after_tripdetail_delete()
RETURNS trigger AS
$BODY$
-- Whenever there are any changes on shipment_tripdetail, interval_from and
-- interval_to will be updated.
DECLARE row_count integer;
BEGIN
    SELECT COUNT(*)
    INTO row_count
    FROM old_table;

    IF row_count < 1 THEN
        RETURN NULL;
    END IF;

    -- Capture are trips that have changes
    WITH cte_a AS (
        SELECT DISTINCT trip_id AS id
        FROM old_table
    ),
    cte_b AS (
        SELECT cte_a.id
        FROM cte_a, shipment_trip
        WHERE cte_a.id = shipment_trip.id
    ),
    cte_c AS (
        SELECT cte_b.id, min_time.interval_from, max_time.interval_to
        FROM cte_b
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_tripdetail
            WHERE trip_id = cte_b.id
            ORDER BY interval_from ASC
            LIMIT 1
        ) min_time ON true
        LEFT JOIN LATERAL (
            SELECT interval_from interval_to
            FROM shipment_tripdetail
            WHERE trip_id = cte_b.id
                AND interval_from > min_time.interval_from
            ORDER BY interval_from DESC
            LIMIT 1
        ) max_time ON true
    )
    UPDATE shipment_trip
    SET interval_from  = cte_c.interval_from,
        interval_to = cte_c.interval_to
    FROM cte_c
    WHERE shipment_trip.id = cte_c.id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trip_refresh_after_tripdetail_delete
ON shipment_tripdetail;
CREATE TRIGGER trip_refresh_after_tripdetail_delete
AFTER DELETE
ON shipment_tripdetail
REFERENCING OLD TABLE AS old_table
FOR EACH STATEMENT EXECUTE PROCEDURE refresh_shipment_trip_after_tripdetail_delete();

CREATE OR REPLACE FUNCTION refresh_shipment_trip_after_tripdetail_insert()
RETURNS trigger AS
$BODY$
-- Whenever there are any changes on shipment_tripdetail, interval_from and
-- interval_to will be updated.
DECLARE row_count integer;
BEGIN
    SELECT COUNT(*)
    INTO row_count
    FROM new_table;

    IF row_count < 1 THEN
        RETURN NULL;
    END IF;

    -- Capture are trips that have changes
    WITH cte_a AS (
        SELECT DISTINCT trip_id AS id
        FROM new_table
    ),
    cte_b AS (
        SELECT cte_a.id
        FROM cte_a, shipment_trip
        WHERE cte_a.id = shipment_trip.id
    ),
    cte_c AS (
        SELECT cte_b.id, min_time.interval_from, max_time.interval_to
        FROM cte_b
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_tripdetail
            WHERE trip_id = cte_b.id
            ORDER BY interval_from ASC
            LIMIT 1
        ) min_time ON true
        LEFT JOIN LATERAL (
            SELECT interval_from interval_to
            FROM shipment_tripdetail
            WHERE trip_id = cte_b.id
                AND interval_from > min_time.interval_from
            ORDER BY interval_from DESC
            LIMIT 1
        ) max_time ON true
    )
    UPDATE shipment_trip
    SET interval_from  = cte_c.interval_from,
        interval_to = cte_c.interval_to
    FROM cte_c
    WHERE shipment_trip.id = cte_c.id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trip_refresh_after_tripdetail_insert
ON shipment_tripdetail;
CREATE TRIGGER trip_refresh_after_tripdetail_insert
AFTER INSERT
ON shipment_tripdetail
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE PROCEDURE refresh_shipment_trip_after_tripdetail_insert();

CREATE OR REPLACE FUNCTION refresh_shipment_trip_after_tripdetail_update()
RETURNS trigger AS
$BODY$
-- Whenever there are any changes on shipment_tripdetail, interval_from and
-- interval_to will be updated.
DECLARE row_count integer;
BEGIN
    WITH changed_table AS (
        SELECT * FROM new_table
        UNION
        SELECT * FROM old_table
    )
    SELECT COUNT(*)
    INTO row_count
    FROM changed_table;

    IF row_count < 1 THEN
        RETURN NULL;
    END IF;

    -- Capture are trips that have changes
    WITH changed_table AS (
        SELECT * FROM new_table
        UNION
        SELECT * FROM old_table
    ), cte_a AS (
        SELECT DISTINCT trip_id AS id
        FROM changed_table
    ),
    cte_b AS (
        SELECT cte_a.id
        FROM cte_a, shipment_trip
        WHERE cte_a.id = shipment_trip.id
    ),
    cte_c AS (
        SELECT cte_b.id, min_time.interval_from, max_time.interval_to
        FROM cte_b
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_tripdetail
            WHERE trip_id = cte_b.id
            ORDER BY interval_from ASC
            LIMIT 1
        ) min_time ON true
        LEFT JOIN LATERAL (
            SELECT interval_from interval_to
            FROM shipment_tripdetail
            WHERE trip_id = cte_b.id
                AND interval_from > min_time.interval_from
            ORDER BY interval_from DESC
            LIMIT 1
        ) max_time ON true
    )
    UPDATE shipment_trip
    SET interval_from  = cte_c.interval_from,
        interval_to = cte_c.interval_to
    FROM cte_c
    WHERE shipment_trip.id = cte_c.id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trip_refresh_after_tripdetail_update
ON shipment_tripdetail;
CREATE TRIGGER trip_refresh_after_tripdetail_update
AFTER UPDATE
ON shipment_tripdetail
REFERENCING NEW TABLE AS new_table OLD TABLE AS old_table
FOR EACH STATEMENT EXECUTE PROCEDURE refresh_shipment_trip_after_tripdetail_update();
