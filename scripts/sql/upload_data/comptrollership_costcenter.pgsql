CREATE TEMPORARY TABLE temp_comptrollership_costcenter
(
    name character varying(40),
    description text
);

\copy temp_comptrollership_costcenter FROM 'data/comptrollership_costcenter.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_costcenter (name, description)
SELECT name, description
FROM temp_comptrollership_costcenter
