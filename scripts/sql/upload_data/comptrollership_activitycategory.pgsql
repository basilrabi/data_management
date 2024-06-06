CREATE TEMPORARY TABLE temp_comptrollership_activitycategory
(
    name character varying(40),
    description text
);

\copy temp_comptrollership_activitycategory FROM 'data/comptrollership_activitycategory.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_activitycategory (name, description)
SELECT name, description
FROM temp_comptrollership_activitycategory

