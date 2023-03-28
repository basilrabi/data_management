CREATE TEMPORARY TABLE temp_custom_profession
(
    name character varying(20),
    description text
);

\copy temp_custom_profession FROM 'data/custom_profession.csv' DELIMITER ',' CSV;

INSERT INTO custom_profession (name, description)
SELECT name, description
FROM temp_custom_profession
