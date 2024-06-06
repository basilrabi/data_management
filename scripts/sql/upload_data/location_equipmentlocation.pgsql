CREATE TEMPORARY TABLE temp_location_equipmentlocation
(
    heading smallint,
    satellites smallint,
    speed smallint,
    time_stamp timestamp with time zone,
    geom text,
    organization character varying(40),
    equipment_class character varying(40),
    fleet_number smallint,
    username character varying(150)
);

\copy temp_location_equipmentlocation FROM 'data/location_equipmentlocation.csv' DELIMITER ',' CSV;

WITH cte_a AS (
    SELECT
        tab_e.id,
        ST_GeomFromEWKT(tab_a.geom) AS geom,
        tab_a.heading,
        tab_a.satellites,
        tab_a.speed,
        tab_a.time_stamp,
        tab_a.username
    FROM temp_location_equipmentlocation tab_a,
        organization_organization tab_c,
        fleet_equipmentclass tab_d,
        fleet_equipment tab_e,
        fleet_equipmentmodel tab_f
    WHERE
        tab_a.organization = tab_c.name AND
        tab_a.equipment_class = tab_d.name AND
        tab_e.owner_id = tab_c.id AND
        tab_e.fleet_number = tab_a.fleet_number AND
        tab_e.model_id = tab_f.id AND
        tab_f.equipment_class_id = tab_d.id
)
INSERT INTO location_equipmentlocation (
    equipment_id,
    geom,
    heading,
    satellites,
    speed,
    time_stamp,
    user_id
)
SELECT
    cte_a.id,
    cte_a.geom,
    cte_a.heading,
    cte_a.satellites,
    cte_a.speed,
    cte_a.time_stamp,
    tab_b.id
FROM cte_a
LEFT JOIN custom_user tab_b
    ON cte_a.username = tab_b.username

