CREATE OR REPLACE FUNCTION insert_dummy_cluster()
RETURNS void AS
$BODY$
DECLARE has_dummy boolean;
BEGIN
    SELECT exists(
        SELECT 1
        FROM location_cluster
        WHERE name = 'XXX'
    )
    INTO has_dummy;
    IF NOT has_dummy THEN
        INSERT INTO location_cluster (name,
                                      z,
                                      ni,
                                      fe,
                                      co,
                                      excavated,
                                      distance_from_road,
                                      with_layout)
        VALUES ('XXX', 0, 0, 0, 0, false, 0, false);
    END IF;
END;
$BODY$ LANGUAGE plpgsql;
