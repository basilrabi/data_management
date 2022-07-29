-- Get the angle between the plane normal and the z-axis
CREATE OR REPLACE FUNCTION slope_angle(geom geometry(PolygonZ))
RETURNS float8 AS
$BODY$
DECLARE
    point_array float8[3][3];
    magnitude float8;
    slope float8;
    v_a float8[3];
    v_b float8[3];
    v_i float8[3];
    v_j float8[3];
    v_k float8[3];
    v_n float8[3];
    v_z float8[3];
BEGIN
    point_array := array_from_geom(geom);
    SELECT ARRAY(SELECT UNNEST(point_array[1:1][1:3])) INTO v_i;
    SELECT ARRAY(SELECT UNNEST(point_array[2:2][1:3])) INTO v_j;
    SELECT ARRAY(SELECT UNNEST(point_array[3:3][1:3])) INTO v_k;
    v_a := subtract_vector(v_j, v_i);
    v_b := subtract_vector(v_k, v_i);
    v_n := cross_product(v_a, v_b);
    v_z := ARRAY[0, 0, 1];
    magnitude := vector_magnitude(v_n);
    IF (magnitude > 0) THEN
        slope := acos(
            (dot_product(v_n, v_z)) / (magnitude * vector_magnitude(v_z))
        );
        IF (slope > (PI() / 2)) THEN
            slope := PI() - slope;
        END IF;
    ELSE
        slope := NULL;
    END IF;

    RETURN slope;
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;
