CREATE TEMPORARY TABLE temp_fleet_engineserialnumber
(
    name character varying (100)
);

\copy temp_fleet_engineserialnumber FROM 'data/fleet_engineserialnumber.csv' DELIMITER ',' CSV;

INSERT INTO fleet_engineserialnumber (name)
SELECT name
FROM temp_fleet_engineserialnumber

