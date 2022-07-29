-- Get the gradient of a surface
CREATE OR REPLACE FUNCTION gradient(geom geometry(PolygonZ))
RETURNS float8 AS
$BODY$
BEGIN
    RETURN tan(slope_angle(geom)) * 100;
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;
