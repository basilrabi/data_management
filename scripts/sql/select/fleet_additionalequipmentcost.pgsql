SELECT
    tab_a.acquisition_cost,
    tab_a.active,
    tab_a.asset_code,
    tab_a.asset_serial_number,
    tab_a.asset_tag_id,
    tab_a.date_acquired,
    tab_a.date_disposal,
    tab_a.date_phased_out,
    tab_a.description,
    tab_a.service_life,
    tab_b.fleet_number,
    tab_d.name owner_name,
    tab_e.name class_name
FROM fleet_additionalequipmentcost tab_a
    LEFT JOIN fleet_equipment tab_b
        ON tab_a.equipment_id = tab_b.id
    LEFT JOIN fleet_equipmentmodel tab_c
        ON tab_b.model_id = tab_c.id
    LEFT JOIN organization_organization tab_d
        ON tab_b.owner_id = tab_d.id
    LEFT JOIN fleet_equipmentclass tab_e
        ON tab_c.equipment_class_id = tab_e.id
ORDER BY
    tab_d.name,
    tab_e.name,
    tab_b.fleet_number,
    tab_a.date_acquired,
    tab_a.description,
    tab_a.asset_code
