SELECT
    tab_a.acquisition_cost,
    tab_a.active,
    tab_a.asset_code,
    tab_a.asset_serial_number,
    tab_a.asset_tag_id,
    tab_a.certificate_of_registration_no,
    tab_a.chassis_serial_number,
    tab_a.cr_date,
    tab_a.date_acquired,
    tab_a.date_disposal,
    tab_a.date_phased_out,
    tab_a.description,
    tab_a.engine_serial_number,
    tab_a.fleet_number,
    tab_a.month_of_registration,
    tab_a.mv_file_no,
    tab_a.plate_number,
    tab_a.service_life,
    tab_a.year_model,
    tab_b.name model_name,
    tab_c.name owner_name,
    tab_d.name class_name,
    tab_e.name manufacturer,
    tab_f.name body_type,
    (regexp_match(tab_g.uid, '^[a-z]+'))[1] unit_class,
    tab_g.name unit_name
FROM fleet_equipment tab_a
    LEFT JOIN fleet_equipmentmodel tab_b
        ON tab_a.model_id = tab_b.id
    LEFT JOIN organization_organization tab_c
        ON tab_a.owner_id = tab_c.id
    LEFT JOIN fleet_equipmentclass tab_d
        ON tab_b.equipment_class_id = tab_d.id
    LEFT JOIN fleet_equipmentmanufacturer tab_e
        ON tab_b.manufacturer_id = tab_e.id
    LEFT JOIN fleet_bodytype tab_f
        ON tab_a.body_type_id = tab_f.id
    LEFT JOIN organization_organizationunit tab_g
        ON tab_a.department_assigned_id = tab_g.id
ORDER BY
    tab_c.name,
    tab_d.name,
    tab_a.fleet_number
