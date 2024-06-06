CREATE TEMPORARY TABLE temp_custom_unitofmeasure
(
    description text,
    name character varying(20)
);

\copy temp_custom_unitofmeasure FROM 'data/custom_unitofmeasure.csv' DELIMITER ',' CSV;

INSERT INTO custom_unitofmeasure (description, name)
SELECT description, name
FROM temp_custom_unitofmeasure

