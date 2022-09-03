CREATE TEMPORARY TABLE temp_material_management_unitofmeasure
(
    name character varying(3),
    description text,
    iso character varying(3),
    unit character varying(3)
);

\copy temp_material_management_unitofmeasure FROM 'data/material_management_unitofmeasure.csv' DELIMITER ',' CSV;

INSERT INTO material_management_unitofmeasure (name, description, iso, unit)
SELECT name, description, iso, unit
FROM temp_material_management_unitofmeasure
