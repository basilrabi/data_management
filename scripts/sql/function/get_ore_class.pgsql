CREATE OR REPLACE FUNCTION get_ore_class(val numeric)
RETURNS text AS
$BODY$
DECLARE ore_class text;
BEGIN
    CASE
        WHEN val >= 2.06 THEN ore_class = 'A';
        WHEN val >= 1.96 THEN ore_class = 'B';
        WHEN val >= 1.81 THEN ore_class = 'C';
        WHEN val >= 1.66 THEN ore_class = 'D';
        WHEN val >= 1.56 THEN ore_class = 'E';
        WHEN val >= 1.45 THEN ore_class = 'F';
        ELSE ore_class = 'W';
    END CASE;
    RETURN ore_class;
END;
$BODY$ LANGUAGE plpgsql;
