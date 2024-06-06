SELECT a.idling,
    a.time_stamp,
    b.fleet_number,
    c.name class_name,
    d.name owner_name
FROM fleet_equipmentidlingtime a,
    fleet_equipment b,
    fleet_equipmentclass c,
    organization_organization d
WHERE a.equipment_id = b.id
    AND b.equipment_class_id = c.id
    AND b.owner_id = d.id
ORDER BY a.time_stamp,
    d.name,
    c.name,
    b.fleet_number

