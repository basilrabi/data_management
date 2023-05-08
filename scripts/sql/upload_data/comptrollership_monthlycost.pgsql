CREATE TEMPORARY TABLE temp_comptrollership_monthlycost
(
    adjusted_budget numeric(13, 2),
    actual numeric(13, 2),
    budget numeric(13, 2),
    forecast numeric(13, 2),
    month smallint,
    remarks text,
    year smallint,
    cost_center character varying(40),
    gl integer
);

\copy temp_comptrollership_monthlycost FROM 'data/comptrollership_monthlycost.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_monthlycost (
    adjusted_budget,
    actual,
    budget,
    forecast,
    month,
    remarks,
    year,
    cost_center_id,
    gl_id
)
SELECT
    tab_a.adjusted_budget,
    tab_a.actual,
    tab_a.budget,
    tab_a.forecast,
    tab_a.month,
    tab_a.remarks,
    tab_a.year,
    tab_b.id,
    tab_c.id
FROM temp_comptrollership_monthlycost tab_a
    LEFT JOIN comptrollership_sapcostcenter tab_b
        ON tab_a.cost_center = tab_b.name
    LEFT JOIN comptrollership_generalledgeraccount tab_c
        ON tab_a.gl = tab_c.code
