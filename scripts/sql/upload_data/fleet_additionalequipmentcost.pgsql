CREATE TEMPORARY TABLE temp_fleet_additionalequipmentcost
(
    acquisition_cost numeric(12,2),
    active boolean,
    asset_code character varying(20),
    asset_serial_number character varying(20),
    asset_tag_id character varying(20),
    date_acquired date,
    date_disposal date,
    date_phased_out date,
    description text,
    service_life smallint,
    fleet_number smallint,
    owner_name character varying(40),
    class_name character varying(40)
);

\copy temp_fleet_additionalequipmentcost FROM 'data/fleet_additionalequipmentcost.csv' DELIMITER ',' CSV;

INSERT INTO fleet_additionalequipmentcost (
    acquisition_cost,
    active,
    asset_code,
    asset_serial_number,
    asset_tag_id,
    date_acquired,
    date_disposal,
    date_phased_out,
    description,
    service_life,
    equipment_id
)
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
    tab_b.id
FROM temp_fleet_additionalequipmentcost tab_a,
    fleet_equipment tab_b,
    fleet_equipmentmodel tab_c,
    organization_organization tab_d,
    fleet_equipmentclass tab_e
WHERE tab_a.fleet_number = tab_b.fleet_number
    AND tab_a.owner_name = tab_d.name
    AND tab_b.owner_id = tab_d.id
    AND tab_a.class_name = tab_e.name
    AND tab_b.model_id = tab_c.id
    AND tab_c.equipment_class_id = tab_e.id
GROUP BY
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
    tab_b.id
