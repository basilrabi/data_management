CREATE TEMPORARY TABLE temp_fleet_equipmentignitionstatus
(
    ignition boolean,
    time_stamp timestamp with time zone,
    fleet_number smallint,
    class_name character varying(40),
    owner_name character varying(40)
);

\copy temp_fleet_equipmentignitionstatus FROM 'data/fleet_equipmentignitionstatus.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentignitionstatus (
    equipment_id,
    ignition,
    time_stamp
)
SELECT
    b.id,
    a.ignition,
    a.time_stamp
FROM temp_fleet_equipmentignitionstatus a,
    fleet_equipment b,
    fleet_equipmentclass c,
    organization_organization d
WHERE a.fleet_number = b.fleet_number
    AND a.class_name = c.name
    AND a.owner_name = d.name
    AND b.equipment_class_id = c.id
    AND b.owner_id = d.id

