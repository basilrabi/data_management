CREATE TEMPORARY TABLE temp_comptrollership_profitcenter
(
    description text,
    name character varying(40)
);

\copy temp_comptrollership_profitcenter FROM 'data/comptrollership_profitcenter.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_profitcenter (
    description,
    name
)
SELECT
    description,
    name
FROM temp_comptrollership_profitcenter

