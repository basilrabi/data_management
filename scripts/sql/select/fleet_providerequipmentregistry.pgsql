SELECT
    tab_a.acquisition_condition,
    tab_a.delivery_year,
    tab_a.pull_out_date,
    tab_a.registration_date,
    tab_a.safety_inspection_id,
    tab_a.sap_registered,
    tab_a.warehouse_registered,
    tab_a.year,
    tab_b.value capacity,
    tab_c.name capacity_unit,
    tab_d.name chassis_serial_number,
    tab_e.name engine_serial_number,
    tab_f.fleet_number,
    tab_g.name equipment_class,
    tab_h.name equipment_model,
    tab_i.name equipment_manufacturer,
    tab_j.plate_number,
    tab_k.name equipment_owner
FROM fleet_providerequipmentregistry tab_a
    LEFT JOIN fleet_capacity tab_b
        ON tab_a.capacity_id = tab_b.id
    LEFT JOIN custom_unitofmeasure tab_c
        ON tab_b.unit_of_measure_id = tab_c.id
    LEFT JOIN fleet_chassisserialnumber tab_d
        ON tab_a.chassis_serial_number_id = tab_d.id
    LEFT JOIN fleet_engineserialnumber tab_e
        ON tab_a.engine_serial_number_id = tab_e.id
    LEFT JOIN fleet_equipment tab_f
        ON tab_a.equipment_id = tab_f.id
    LEFT JOIN fleet_equipmentclass tab_g
        ON tab_f.equipment_class_id = tab_g.id
    LEFT JOIN fleet_equipmentmodel tab_h
        ON tab_a.model_id = tab_h.id
    LEFT JOIN fleet_equipmentmanufacturer tab_i
        ON tab_h.manufacturer_id = tab_i.id
    LEFT JOIN fleet_platenumber tab_j
        ON tab_a.plate_number_id = tab_j.id
    LEFT JOIN organization_organization tab_k
        ON tab_f.owner_id = tab_k.id
ORDER BY tab_a.registration_date,
    tab_k.name,
    tab_g.name,
    tab_f.fleet_number

