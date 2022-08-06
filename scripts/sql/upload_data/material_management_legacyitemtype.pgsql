CREATE TEMPORARY TABLE temp_material_management_legacyitemtype
(
    name character varying(40),
    description text
);

\copy temp_material_management_legacyitemtype FROM 'data/material_management_legacyitemtype.csv' DELIMITER ',' CSV;

INSERT INTO material_management_legacyitemtype (name, description)
SELECT name, description
FROM temp_material_management_legacyitemtype
