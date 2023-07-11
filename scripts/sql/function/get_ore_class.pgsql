CREATE OR REPLACE FUNCTION get_ore_class(ni numeric, fe numeric)
RETURNS character(1) AS
$BODY$
DECLARE ore_class text;
BEGIN
    CASE
        WHEN ni >= 1.81 THEN ore_class = 'A';
        WHEN ni >= 1.66 THEN ore_class = 'B';
        WHEN ni >= 1.56 THEN ore_class = 'C';
        WHEN ni >= 1.45 THEN ore_class = 'D';
        WHEN ni >= 1.35 THEN ore_class = 'E';
        WHEN ni >= 1.20 THEN ore_class = 'F';
        WHEN ni < 1.20 AND fe >= 40 THEN ore_class = 'L';
        ELSE ore_class = 'W';
    END CASE;
    RETURN ore_class;
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;
