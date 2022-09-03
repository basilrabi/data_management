CREATE TEMPORARY TABLE temp_material_management_materialtype
(
    name character varying(40),
    description text
);

\copy temp_material_management_materialtype FROM 'data/material_management_materialtype.csv' DELIMITER ',' CSV;

INSERT INTO material_management_materialtype (name, description)
SELECT name, description
FROM temp_material_management_materialtype
