CREATE TEMPORARY TABLE temp_fleet_equipmentclass
(
    name character varying(20),
    description text
);

\copy temp_fleet_equipmentclass FROM 'data/fleet_equipmentclass.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentclass (name, description)
SELECT name, description
FROM temp_fleet_equipmentclass
