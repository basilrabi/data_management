CREATE TEMPORARY TABLE temp_comptrollership_material
(
    name character varying(40),
    description text
);

\copy temp_comptrollership_material FROM 'data/comptrollership_material.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_material (name, description)
SELECT name, description
FROM temp_comptrollership_material

