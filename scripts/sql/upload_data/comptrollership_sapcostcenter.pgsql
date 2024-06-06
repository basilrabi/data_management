CREATE TEMPORARY TABLE temp_comptrollership_sapcostcenter
(
    description text,
    long_name text,
    name character varying(40),
    remarks text,
    profit_center character varying(40)
);

\copy temp_comptrollership_sapcostcenter FROM 'data/comptrollership_sapcostcenter.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_sapcostcenter (
    description,
    long_name,
    name,
    remarks,
    profit_center_id
)
SELECT
    a.description,
    a.long_name,
    a.name,
    a.remarks,
    b.id
FROM temp_comptrollership_sapcostcenter a
LEFT JOIN comptrollership_profitcenter b
    ON a.profit_center = b.name

