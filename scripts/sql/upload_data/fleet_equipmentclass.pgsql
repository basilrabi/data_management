CREATE TEMPORARY TABLE temp_fleet_equipmentclass
(
    code character varying (1),
    description text,
    name character varying (40)
);

\copy temp_fleet_equipmentclass FROM 'data/fleet_equipmentclass.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentclass (
    code,
    description,
    name
)
SELECT
    code,
    description,
    name
FROM temp_fleet_equipmentclass

