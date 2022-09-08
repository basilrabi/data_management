CREATE TEMPORARY TABLE temp_material_management_material
(
    name character varying(40),
    description text,
    part_number text,
    group_name character varying(40),
    type_name character varying(40),
    unit_name character varying(40),
    valuation smallint
);

\copy temp_material_management_material FROM 'data/material_management_material.csv' DELIMITER ',' CSV;

INSERT INTO material_management_material (
    name,
    description,
    part_number,
    group_id,
    type_id,
    unit_of_measure_id,
    valuation_id
)
SELECT
    tab_a.name,
    tab_a.description,
    tab_a.part_number,
    tab_b.id,
    tab_c.id,
    tab_d.id,
    tab_e.id
FROM temp_material_management_material tab_a
    LEFT JOIN material_management_materialgroup tab_b
        ON tab_a.group_name = tab_b.name
    LEFT JOIN material_management_materialtype tab_c
        ON tab_a.type_name = tab_c.name
    LEFT JOIN material_management_unitofmeasure tab_d
        ON tab_a.unit_name = tab_d.unit
    LEFT JOIN material_management_valuation tab_e
        ON tab_a.valuation = tab_e.name
