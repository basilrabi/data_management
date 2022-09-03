CREATE TEMPORARY TABLE temp_material_management_materialgroup
(
    name character varying(40),
    description text,
    long_description text
);

\copy temp_material_management_materialgroup FROM 'data/material_management_materialgroup.csv' DELIMITER ',' CSV;

INSERT INTO material_management_materialgroup (
    name, description, long_description
)
SELECT name, description, long_description
FROM temp_material_management_materialgroup
