CREATE TEMPORARY TABLE temp_sampling_laboratory
(
    name character varying(40),
    description text
);

\copy temp_sampling_laboratory FROM 'data/sampling_laboratory.csv' DELIMITER ',' CSV;

INSERT INTO sampling_laboratory (name, description)
SELECT name, description
FROM temp_sampling_laboratory
