CREATE TEMPORARY TABLE temp_sampling_lithology
(
    name character varying(20),
    description text
);

\copy temp_sampling_lithology FROM 'data/sampling_lithology.csv' DELIMITER ',' CSV;

INSERT INTO sampling_lithology (name, description)
SELECT name, description
FROM temp_sampling_lithology
