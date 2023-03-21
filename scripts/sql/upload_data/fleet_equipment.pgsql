CREATE TEMPORARY TABLE temp_fleet_equipment
(
    fleet_number smallint,
    acquisition_cost numeric(12,2),
    acquisition_cost_from_accounting numeric(12,2),
    date_acquired date,
    date_phased_out date,
    date_disposal date,
    engine_serial_number character varying(100),
    plate_number character varying(20),
    chassis_serial_number character varying(100),
    active boolean,
    model_name character varying(40),
    class_name character varying(40),
    manufacturer character varying(40),
    owner_name character varying(40)
);

\copy temp_fleet_equipment FROM 'data/fleet_equipment.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipment (
    fleet_number,
    acquisition_cost,
    acquisition_cost_from_accounting,
    date_acquired,
    date_phased_out,
    date_disposal,
    engine_serial_number,
    plate_number,
    chassis_serial_number,
    active,
    model_id,
    owner_id,
    equipment_class_id
)
SELECT
    tab_a.fleet_number,
    tab_a.acquisition_cost,
    tab_a.acquisition_cost_from_accounting,
    tab_a.date_acquired,
    tab_a.date_phased_out,
    tab_a.date_disposal,
    tab_a.engine_serial_number,
    tab_a.plate_number,
    tab_a.chassis_serial_number,
    tab_a.active,
    tab_b.id,
    tab_c.id,
    tab_b.equipment_class_id
FROM temp_fleet_equipment tab_a,
    fleet_equipmentmodel tab_b,
    organization_organization tab_c,
    fleet_equipmentmodel tab_d,
    fleet_equipmentmanufacturer tab_e,
    fleet_equipmentclass tab_f
WHERE tab_a.model_name = tab_b.name
    AND tab_a.owner_name = tab_c.name
    AND tab_a.manufacturer = tab_e.name
    AND tab_a.class_name = tab_f.name
    AND tab_b.equipment_class_id = tab_f.id
    AND tab_b.manufacturer_id = tab_e.id
GROUP BY
    tab_a.fleet_number,
    tab_a.acquisition_cost,
    tab_a.acquisition_cost_from_accounting,
    tab_a.date_acquired,
    tab_a.date_phased_out,
    tab_a.date_disposal,
    tab_a.engine_serial_number,
    tab_a.plate_number,
    tab_a.chassis_serial_number,
    tab_a.active,
    tab_b.id,
    tab_c.id,
    tab_b.equipment_class_id
