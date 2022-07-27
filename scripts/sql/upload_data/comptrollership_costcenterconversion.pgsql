CREATE TEMPORARY TABLE temp_comptrollership_costcenterconversion
(
    old_code character varying(40),
    sap_code character varying(40)
);

\copy temp_comptrollership_costcenterconversion FROM 'data/comptrollership_costcenterconversion.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_costcenterconversion (old_cost_center_id, sap_cost_center_id)
SELECT b.id, c.id
FROM temp_comptrollership_costcenterconversion a
    LEFT JOIN comptrollership_costcenter b
        ON a.old_code = b.name
    LEFT JOIN comptrollership_sapcostcenter c
        ON a.sap_code = c.name
