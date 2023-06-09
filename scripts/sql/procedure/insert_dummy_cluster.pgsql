CREATE OR REPLACE PROCEDURE insert_dummy_cluster()
AS
$BODY$
DECLARE has_dummy boolean;
BEGIN
    SELECT exists(
        SELECT 1
        FROM location_cluster
        WHERE name = '111'
    )
    INTO has_dummy;
    IF NOT has_dummy THEN
        INSERT INTO location_cluster (
            name,
            z,
            ni,
            fe,
            co,
            excavated,
            distance_from_road,
            modified
        )
        VALUES ('111', 0, 0, 0, 0, false, 0, NOW());
    END IF;
END;
$BODY$
LANGUAGE plpgsql;
