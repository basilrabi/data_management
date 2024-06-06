SELECT
    tab_a.number,
    tab_a.spaceless_number,
    tab_b.fleet_number,
    tab_c.name equipment_class,
    tab_d.name owner_name
FROM fleet_equipmentmobilenumber tab_a,
    fleet_equipment tab_b,
    fleet_equipmentclass tab_c,
    organization_organization tab_d
WHERE tab_a.equipment_id = tab_b.id
    AND tab_b.equipment_class_id = tab_c.id
    AND tab_b.owner_id = tab_d.id
ORDER BY tab_a.number

