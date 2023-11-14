CREATE TEMPORARY TABLE temp_fleet_equipmentidlingtime
(
    idling boolean,
    time_stamp timestamp with time zone,
    fleet_number smallint,
    class_name character varying(40),
    owner_name character varying(40)
);

\copy temp_fleet_equipmentidlingtime FROM 'data/fleet_equipmentidlingtime.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentidlingtime (
    equipment_id,
    idling,
    time_stamp
)
SELECT
    b.id,
    a.idling,
    a.time_stamp
FROM temp_fleet_equipmentidlingtime a,
    fleet_equipment b,
    fleet_equipmentclass c,
    organization_organization d
WHERE a.fleet_number = b.fleet_number
    AND a.class_name = c.name
    AND a.owner_name = d.name
    AND b.equipment_class_id = c.id
    AND b.owner_id = d.id

