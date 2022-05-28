CREATE TEMPORARY TABLE temp_fleet_equipmentmanufacturer
(
    name character varying(40),
    description text
);

\copy temp_fleet_equipmentmanufacturer FROM 'data/fleet_equipmentmanufacturer.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentmanufacturer (name, description)
SELECT name, description
FROM temp_fleet_equipmentmanufacturer
