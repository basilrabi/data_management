SELECT
    tab_a.fleet_number,
    tab_a.acquisition_cost,
    tab_a.acquisition_cost_from_accounting,
    tab_a.date_acquired,
    tab_a.date_phased_out,
    REGEXP_REPLACE(tab_a.serial_number, '[^\w]', '', 'g') serial_number,
    tab_b.name model_name,
    tab_d.name class_name,
    tab_e.name manufacturer,
    tab_c.name owner_name
FROM fleet_equipment tab_a
    LEFT JOIN fleet_equipmentmodel tab_b
        ON tab_a.model_id = tab_b.id
    LEFT JOIN organization_organization tab_c
        ON tab_a.owner_id = tab_c.id
    LEFT JOIN fleet_equipmentclass tab_d
        ON tab_b.equipment_class_id = tab_d.id
    LEFT JOIN fleet_equipmentmanufacturer tab_e
        ON tab_b.manufacturer_id = tab_e.id
ORDER BY
    tab_c.name,
    tab_d.name,
    tab_a.fleet_number
