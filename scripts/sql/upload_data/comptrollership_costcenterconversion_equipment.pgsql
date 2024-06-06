CREATE TEMPORARY TABLE temp_comptrollership_costcenterconversion_equipment
(
    old_cost_center character varying(40),
    sap_cost_center character varying(40),
    equipment_class character varying(40)
);

\copy temp_comptrollership_costcenterconversion_equipment FROM 'data/comptrollership_costcenterconversion_equipment.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_costcenterconversion_equipment (
    costcenterconversion_id,
    equipmentclass_id
)
SELECT tab_c.id, tab_e.id
FROM temp_comptrollership_costcenterconversion_equipment tab_a,
    comptrollership_costcenter tab_b,
    comptrollership_costcenterconversion tab_c,
    comptrollership_sapcostcenter tab_d,
    fleet_equipmentclass tab_e
WHERE tab_a.equipment_class = tab_e.name
    AND tab_a.old_cost_center = tab_b.name
    AND tab_a.sap_cost_center = tab_d.name
    AND tab_b.id = tab_c.old_cost_center_id
    AND tab_c.sap_cost_center_id = tab_d.id

