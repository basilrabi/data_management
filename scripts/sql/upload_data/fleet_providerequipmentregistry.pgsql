CREATE TEMPORARY TABLE temp_fleet_providerequipmentregistry
(
    acquisition_condition boolean,
    delivery_year smallint,
    pull_out_date date,
    registration_date date,
    safety_inspection_id smallint,
    sap_registered boolean,
    warehouse_registered boolean,
    year smallint,
    capacity numeric (10, 2),
    capacity_unit character varying (40),
    chassis_serial_number character varying (100),
    engine_serial_number character varying (100),
    fleet_number smallint,
    equipment_class character varying (40),
    equipment_model character varying (40),
    equipment_manufacturer character varying (40),
    plate_number character varying (10),
    equipment_owner character varying (40)
);

\copy temp_fleet_providerequipmentregistry FROM 'data/fleet_providerequipmentregistry.csv' DELIMITER ',' CSV;

INSERT INTO fleet_providerequipmentregistry (
    acquisition_condition,
    capacity_id,
    chassis_serial_number_id,
    delivery_year,
    engine_serial_number_id,
    equipment_id,
    model_id,
    plate_number_id,
    pull_out_date,
    registration_date,
    safety_inspection_id,
    sap_registered,
    warehouse_registered,
    x_contractor,
    x_equipment_class,
    year
)
SELECT
    tab_a.acquisition_condition,
    tab_c.id,
    tab_d.id,
    tab_a.delivery_year,
    tab_e.id,
    tab_h.id,
    tab_j.id,
    tab_k.id,
    tab_a.pull_out_date,
    tab_a.registration_date,
    tab_a.safety_inspection_id,
    tab_a.sap_registered,
    tab_a.warehouse_registered,
    tab_a.equipment_owner,
    tab_a.equipment_class,
    tab_a.year
FROM temp_fleet_providerequipmentregistry tab_a
    LEFT JOIN custom_unitofmeasure tab_b
        ON tab_a.capacity_unit = tab_b.name
    LEFT JOIN fleet_capacity tab_c
        ON tab_a.capacity = tab_c.value
            AND tab_b.id = tab_c.unit_of_measure_id
    LEFT JOIN fleet_chassisserialnumber tab_d
        ON tab_a.chassis_serial_number = tab_d.name
    LEFT JOIN fleet_engineserialnumber tab_e
        ON tab_a.engine_serial_number = tab_e.name
    LEFT JOIN fleet_equipmentclass tab_f
        ON tab_a.equipment_class = tab_f.name
    LEFT JOIN organization_organization tab_g
        ON tab_a.equipment_owner = tab_g.name
    LEFT JOIN fleet_equipment tab_h
        ON tab_a.fleet_number = tab_h.fleet_number
            AND tab_f.id = tab_h.equipment_class_id
            AND tab_g.id = tab_h.owner_id
    LEFT JOIN fleet_equipmentmanufacturer tab_i
        ON tab_a.equipment_manufacturer = tab_i.name
    LEFT JOIN fleet_equipmentmodel tab_j
        ON tab_a.equipment_model = tab_j.name
            AND tab_f.id = tab_j.equipment_class_id
            AND tab_i.id = tab_j.manufacturer_id
    LEFT JOIN fleet_platenumber tab_k
        ON tab_a.plate_number = tab_k.plate_number

