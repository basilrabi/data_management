CREATE TEMPORARY TABLE temp_fleet_bodytype
(
    name character varying(40),
    description text
);

\copy temp_fleet_bodytype FROM 'data/fleet_bodytype.csv' DELIMITER ',' CSV;

INSERT INTO fleet_bodytype (name, description)
SELECT name, description
FROM temp_fleet_bodytype
