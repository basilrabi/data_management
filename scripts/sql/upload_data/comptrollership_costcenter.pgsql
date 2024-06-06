CREATE TEMPORARY TABLE temp_comptrollership_costcenter
(
    description text,
    name character varying(40),
    material character varying(40)
);

\copy temp_comptrollership_costcenter FROM 'data/comptrollership_costcenter.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_costcenter (
    description,
    name,
    material_id
)
SELECT
    tab_a.description,
    tab_a.name,
    tab_b.id
FROM temp_comptrollership_costcenter tab_a
    LEFT JOIN comptrollership_material tab_b
        ON tab_a.material = tab_b.name

