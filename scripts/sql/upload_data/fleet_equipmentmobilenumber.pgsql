CREATE TEMPORARY TABLE temp_fleet_equipmentmobilenumber
(
    "number" character varying (128),
    spaceless_number character varying (20),
    fleet_number smallint,
    equipment_class character varying (40),
    owner_name character varying (40)
);

\copy temp_fleet_equipmentmobilenumber FROM 'data/fleet_equipmentmobilenumber.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentmobilenumber (
    equipment_id,
    "number",
    spaceless_number
)
SELECT
    tab_b.id,
    tab_a."number",
    tab_a.spaceless_number
FROM temp_fleet_equipmentmobilenumber tab_a,
    fleet_equipment tab_b,
    fleet_equipmentclass tab_c,
    organization_organization tab_d
WHERE tab_a.equipment_class = tab_c.name
    AND tab_a.fleet_number = tab_b.fleet_number
    AND tab_a.owner_name = tab_d.name
    AND tab_b.equipment_class_id = tab_c.id
    AND tab_b.owner_id = tab_d.id

