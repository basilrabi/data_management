CREATE TEMPORARY TABLE temp_fleet_equipmentmodel
(
    name character varying(40),
    description text,
    equipment_class character varying(40),
    manufacturer character varying(40)
);

\copy temp_fleet_equipmentmodel FROM 'data/fleet_equipmentmodel.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipmentmodel (
    name,
    description,
    equipment_class_id,
    manufacturer_id
)
SELECT
    a.name,
    a.description,
    b.id,
    c.id
FROM temp_fleet_equipmentmodel a
    LEFT JOIN fleet_equipmentclass b
        ON a.equipment_class = b.name
    LEFT JOIN fleet_equipmentmanufacturer c
        ON a.manufacturer = c.name;
