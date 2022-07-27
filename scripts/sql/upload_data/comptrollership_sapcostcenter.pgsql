CREATE TEMPORARY TABLE temp_comptrollership_sapcostcenter
(
    name character varying(40),
    description text,
    long_name character varying(40),
    remarks text
);

\copy temp_comptrollership_sapcostcenter FROM 'data/comptrollership_sapcostcenter.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_sapcostcenter (
    name,
    description,
    long_name,
    remarks
)
SELECT
    name,
    description,
    long_name,
    remarks
FROM temp_comptrollership_sapcostcenter
