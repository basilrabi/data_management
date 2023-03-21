-- Convert a PolygonZ to an array of its first 3 points.
CREATE OR REPLACE FUNCTION array_from_geom(input_geom geometry(PolygonZ))
RETURNS float8[3][3] AS
$BODY$
DECLARE out float8[3][3];
BEGIN
    WITH cte_a AS (SELECT * FROM ST_DumpPoints(input_geom)),
    cte_b AS (
        SELECT ST_X(geom) x, ST_Y(geom) y, ST_Z(geom) z
        FROM cte_a WHERE path[2] IN (1, 2, 3)
    )
    SELECT array_agg(array[x, y, z]) INTO out
    FROM cte_b;
    RETURN out;
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;
