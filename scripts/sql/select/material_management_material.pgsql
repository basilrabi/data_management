SELECT
    tab_a.name,
    tab_a.description,
    tab_a.part_number,
    tab_b.name group_name,
    tab_c.name type_name,
    tab_d.unit unit_name,
    tab_e.name valuation
FROM material_management_material tab_a
    LEFT JOIN material_management_materialgroup tab_b
        ON tab_a.group_id = tab_b.id
    LEFT JOIN material_management_materialtype tab_c
        ON tab_a.type_id = tab_c.id
    LEFT JOIN material_management_unitofmeasure tab_d
        ON tab_a.unit_of_measure_id = tab_d.id
    LEFT JOIN material_management_valuation tab_e
        ON tab_a.valuation_id = tab_e.id
ORDER BY tab_a.name
