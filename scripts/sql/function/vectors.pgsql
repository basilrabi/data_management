-- Various functions for 3D vector operations

CREATE OR REPLACE FUNCTION add_vector(v_a float8[3], v_b float8[3])
RETURNS float8[3] AS
$BODY$
BEGIN
    RETURN ARRAY[v_a[1] + v_b[1], v_a[2] + v_b[2], v_a[3] + v_b[3]];
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;

CREATE OR REPLACE FUNCTION cross_product(v_a float8[3], v_b float8[3])
RETURNS float8[3] AS
$BODY$
BEGIN
    RETURN ARRAY[
        (v_a[2] * v_b[3]) - (v_a[3] * v_b[2]),
        (v_a[3] * v_b[1]) - (v_a[1] * v_b[3]),
        (v_a[1] * v_b[2]) - (v_a[2] * v_b[1])
    ];
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;

CREATE OR REPLACE FUNCTION dot_product(v_a float8[3], v_b float8[3])
RETURNS float8 AS
$BODY$
BEGIN
    RETURN (v_a[1] * v_b[1]) + (v_a[2] * v_b[2]) + (v_a[3] * v_b[3]);
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;

CREATE OR REPLACE FUNCTION subtract_vector(v_a float8[3], v_b float8[3])
RETURNS float8[3] AS
$BODY$
BEGIN
    RETURN ARRAY[v_a[1] - v_b[1], v_a[2] - v_b[2], v_a[3] - v_b[3]];
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;

CREATE OR REPLACE FUNCTION vector_magnitude(v_a float8[3])
RETURNS float8 AS
$BODY$
BEGIN
    RETURN POWER(POWER(v_a[1], 2) + POWER(v_a[2], 2) + POWER(v_a[3], 2), 0.5);
END;
$BODY$
LANGUAGE plpgsql
IMMUTABLE;
