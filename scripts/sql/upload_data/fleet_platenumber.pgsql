CREATE TEMPORARY TABLE temp_fleet_platenumber
(
    plate_number character varying (10)
);

\copy temp_fleet_platenumber FROM 'data/fleet_platenumber.csv' DELIMITER ',' CSV;

INSERT INTO fleet_platenumber (plate_number)
SELECT plate_number
FROM temp_fleet_platenumber

