CREATE TEMPORARY TABLE temp_comptrollership_activitycode
(
    name character varying(40),
    description text
);

\copy temp_comptrollership_activitycode FROM 'data/comptrollership_activitycode.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_activitycode (name, description)
SELECT name, description
FROM temp_comptrollership_activitycode

