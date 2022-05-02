CREATE TEMPORARY TABLE temp_location_equipmentlocation
(
    time_stamp timestamp with time zone,
    geom text,
    organization character varying(20),
    equipment_class character varying(20),
    fleet_number smallint,
    username character varying(150)
);

\copy temp_location_equipmentlocation FROM 'data/location_equipmentlocation.csv' DELIMITER ',' CSV;

INSERT INTO location_equipmentlocation (
    equipment_id,
    geom,
    time_stamp,
    user_id
)
SELECT
    tab_e.id,
    ST_GeomFromEWKT(tab_a.geom),
    tab_a.time_stamp,
    tab_b.id
FROM
    temp_location_equipmentlocation tab_a,
    custom_user tab_b,
    organization_organization tab_c,
    fleet_equipmentclass tab_d,
    fleet_equipment tab_e,
    fleet_equipmentmodel tab_f
WHERE
    tab_a.username = tab_b.username AND
    tab_a.organization = tab_c.name AND
    tab_a.equipment_class = tab_d.name AND
    tab_e.owner_id = tab_c.id AND
    tab_e.fleet_number = tab_a.fleet_number AND
    tab_e.model_id = tab_f.id AND
    tab_f.equipment_class_id = tab_d.id
