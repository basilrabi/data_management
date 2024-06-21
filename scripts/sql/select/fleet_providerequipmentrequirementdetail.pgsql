SELECT
    tab_a.activity,
    tab_a.running,
    tab_a.with_spare,
    tab_b.year,
    tab_c.name equipment,
    tab_d.name contractor
FROM fleet_providerequipmentrequirementdetail tab_a,
    fleet_providerequipmentrequirement tab_b,
    fleet_equipmentclass tab_c,
    organization_organization tab_d
WHERE tab_a.requirement_id = tab_b.id
    AND tab_a.equipment_id = tab_c.id
    AND tab_b.contractor_id = tab_d.id
ORDER BY tab_b.year DESC,
    tab_d.name,
    tab_c.name

