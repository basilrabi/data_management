SELECT
    a.fleet_number,
    a.acquisition_cost,
    a.date_acquired,
    a.date_phased_out,
    a.serial_number,
    b.name model_name,
    c.name owner_name
FROM fleet_equipment a
    LEFT JOIN fleet_equipmentmodel b
        ON a.model_id = b.id
    LEFT JOIN organization_organization c
        ON a.owner_id = c.id
    LEFT JOIN fleet_equipmentclass d
        ON b.equipment_class_id = d.id
ORDER BY
    c.name,
    d.name,
    a.fleet_number
