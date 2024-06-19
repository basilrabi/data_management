SELECT
    tab_a.registration_date,
    tab_c.name company,
    tab_d.name equipment_type,
    LPAD(tab_b.fleet_number::text, 3, '0') AS number,
    FORMAT(
        '%s %s-%s',
        tab_c.name,
        tab_d.name,
        LPAD(tab_b.fleet_number::text, 3, '0')
    ) equipment,
    FORMAT(
        '%s-%s',
        EXTRACT(year FROM tab_a.registration_date)::text,
        LPAD(tab_a.safety_inspection_id::text, 4, '0')
    ) safety_number,
    tab_f.name equipment_make,
    tab_e.name equipment_model,
    tab_g.name enginer_serial_number,
    tab_h.name chassis_serial_number,
    tab_i.plate_number,
    tab_a.delivery_year year_acquired,
    CASE
        WHEN tab_a.acquisition_condition THEN 'Used'
        ELSE 'New'
    END condition_during_acquisition,
    tab_j.value::text || ' ' || tab_k.name AS capacity,
    CASE
        WHEN tab_a.pull_out_date IS NULL THEN 'REGISTERED'
        ELSE 'PULLED-OUT'
    END remarks,
    tab_a.pull_out_date,
    FORMAT(
        '03C%s%s%s',
        tab_c.resource_code,
        tab_d.code,
        LPAD(tab_b.fleet_number::text, 3, '0')
    ) resource,
    FORMAT(
        '%s-%s%s-%s-C',
        tab_c.warehouse_code,
        tab_d.name,
        RIGHT(tab_a.delivery_year::text, 2),
        LPAD(tab_b.fleet_number::text, 3, '0')
    ) warehouse_code,
    FORMAT(
        '%s-%s%s-%s',
        tab_c.name,
        tab_d.name,
        RIGHT(tab_a.delivery_year::text, 2),
        LPAD(tab_b.fleet_number::text, 3, '0')
    ) omt_code
FROM fleet_providerequipmentregistry tab_a
    LEFT JOIN fleet_equipment tab_b
        ON tab_a.equipment_id = tab_b.id
    LEFT JOIN organization_organization tab_c
        ON tab_b.owner_id = tab_c.id
    LEFT JOIN fleet_equipmentclass tab_d
        ON tab_b.equipment_class_id = tab_d.id
    LEFT JOIN fleet_equipmentmodel tab_e
        ON tab_b.model_id = tab_e.id
    LEFT JOIN fleet_equipmentmanufacturer tab_f
        ON tab_e.manufacturer_id = tab_f.id
    LEFT JOIN fleet_engineserialnumber tab_g
        ON tab_a.engine_serial_number_id = tab_g.id
    LEFT JOIN fleet_chassisserialnumber tab_h
        ON tab_a.chassis_serial_number_id = tab_h.id
    LEFT JOIN fleet_platenumber tab_i
        ON tab_a.plate_number_id = tab_i.id
    LEFT JOIN fleet_capacity tab_j
        ON tab_a.capacity_id = tab_j.id
    LEFT JOIN custom_unitofmeasure tab_k
        ON tab_j.unit_of_measure_id = tab_k.id

