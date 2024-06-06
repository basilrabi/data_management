SELECT
    tab_c.name old_cost_center,
    tab_d.name sap_cost_center,
    tab_e.name equipment_class
FROM comptrollership_costcenterconversion_equipment tab_a,
    comptrollership_costcenterconversion tab_b,
    comptrollership_costcenter tab_c,
    comptrollership_sapcostcenter tab_d,
    fleet_equipmentclass tab_e
WHERE tab_a.costcenterconversion_id = tab_b.id
    AND tab_a.equipmentclass_id = tab_e.id
    AND tab_b.old_cost_center_id = tab_c.id
    AND tab_b.sap_cost_center_id = tab_d.id
ORDER BY
    tab_d.name,
    tab_c.name,
    tab_e.name

