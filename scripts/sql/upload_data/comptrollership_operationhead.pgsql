CREATE TEMPORARY TABLE temp_comptrollership_operationhead
(
    name character varying(40),
    description text
);

\copy temp_comptrollership_operationhead FROM 'data/comptrollership_operationhead.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_operationhead (name, description)
SELECT name, description
FROM temp_comptrollership_operationhead

