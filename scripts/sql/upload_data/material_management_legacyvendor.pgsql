CREATE TEMPORARY TABLE temp_material_management_legacyvendor
(
    name character varying(40),
    description text
);

\copy temp_material_management_legacyvendor FROM 'data/material_management_legacyvendor.csv' DELIMITER ',' CSV;

INSERT INTO material_management_legacyvendor (name, description)
SELECT name, description
FROM temp_material_management_legacyvendor
