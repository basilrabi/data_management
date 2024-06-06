CREATE TEMPORARY TABLE temp_fleet_chassisserialnumber
(
    name character varying (100)
);

\copy temp_fleet_chassisserialnumber FROM 'data/fleet_chassisserialnumber.csv' DELIMITER ',' CSV;

INSERT INTO fleet_chassisserialnumber (name)
SELECT name
FROM temp_fleet_chassisserialnumber

