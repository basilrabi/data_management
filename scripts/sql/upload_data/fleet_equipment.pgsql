CREATE TEMPORARY TABLE temp_fleet_equipment
(
    acquisition_cost numeric(12,2),
    active boolean,
    asset_code character varying(20),
    asset_serial_number character varying(20),
    asset_tag_id character varying(20),
    certificate_of_registration_no character varying(30),
    chassis_serial_number character varying(100),
    cr_date date,
    date_acquired date,
    date_disposal date,
    date_phased_out date,
    department_assigned text,
    description text,
    engine_serial_number character varying(100),
    fleet_number smallint,
    month_of_registration character varying(20),
    mv_file_no character varying(30),
    plate_number character varying(20),
    service_life smallint,
    year_model smallint,
    model_name character varying(40),
    owner_name character varying(40),
    class_name character varying(40),
    manufacturer character varying(40),
    body_type character varying(40)
);

\copy temp_fleet_equipment FROM 'data/fleet_equipment.csv' DELIMITER ',' CSV;

WITH cte_a AS (
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
        tab_b.id fleet_equipmentmodel_id,
        tab_c.id organization_organization_id,
        tab_b.equipment_class_id,
        tab_a.body_type
    FROM temp_fleet_equipment tab_a,
        fleet_equipmentmodel tab_b,
        organization_organization tab_c,
        fleet_equipmentmanufacturer tab_d,
        fleet_equipmentclass tab_e
    WHERE tab_a.model_name = tab_b.name
        AND tab_a.owner_name = tab_c.name
        AND tab_a.model_name = tab_b.name
        AND tab_a.manufacturer = tab_d.name
        AND tab_a.class_name = tab_e.name
        AND tab_b.equipment_class_id = tab_e.id
        AND tab_b.manufacturer_id = tab_d.id
    GROUP BY
        tab_a.acquisition_cost,
        tab_a.active,
        tab_a.asset_code,
        tab_a.asset_serial_number,
        tab_a.asset_tag_id,
        tab_a.body_type,
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
        tab_b.id,
        tab_c.id,
        tab_b.equipment_class_id
),
cte_b AS (
    SELECT cte_a.*, bt.id body_type_id
    FROM cte_a
    LEFT JOIN fleet_bodytype bt
        ON cte_a.body_type = bt.name
)
INSERT INTO fleet_equipment (
    acquisition_cost,
    active,
    asset_code,
    asset_serial_number,
    asset_tag_id,
    certificate_of_registration_no,
    chassis_serial_number,
    cr_date,
    date_acquired,
    date_disposal,
    date_phased_out,
    description,
    engine_serial_number,
    fleet_number,
    month_of_registration,
    mv_file_no,
    plate_number,
    service_life,
    year_model,
    model_id,
    owner_id,
    equipment_class_id,
    body_type_id
)
SELECT
    acquisition_cost,
    active,
    asset_code,
    asset_serial_number,
    asset_tag_id,
    certificate_of_registration_no,
    chassis_serial_number,
    cr_date,
    date_acquired,
    date_disposal,
    date_phased_out,
    description,
    engine_serial_number,
    fleet_number,
    month_of_registration,
    mv_file_no,
    plate_number,
    service_life,
    year_model,
    fleet_equipmentmodel_id,
    organization_organization_id,
    equipment_class_id,
    body_type_id
FROM cte_b
