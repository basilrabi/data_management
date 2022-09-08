CREATE TEMPORARY TABLE temp_material_management_valuation
(
    name smallint,
    description text,
    gl integer
);

\copy temp_material_management_valuation FROM 'data/material_management_valuation.csv' DELIMITER ',' CSV;

INSERT INTO material_management_valuation (name, description, gl_id)
SELECT a.name, a.description, b.id
FROM temp_material_management_valuation a
    LEFT JOIN comptrollership_generalledgeraccount b
        ON a.gl = b.code
