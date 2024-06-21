CREATE TEMPORARY TABLE temp_fleet_providerequipmentrequirementdetail
(
    activity character varying (1),
    running smallint,
    with_spare smallint,
    year smallint,
    equipment character varying (40),
    contractor character varying (40)
);

\copy temp_fleet_providerequipmentrequirementdetail FROM 'data/fleet_providerequipmentrequirementdetail.csv' DELIMITER ',' CSV;

INSERT INTO fleet_providerequipmentrequirementdetail (
    activity,
    equipment_id,
    requirement_id,
    running,
    with_spare
)
SELECT
    tab_a.activity,
    tab_b.id,
    tab_d.id,
    tab_a.running,
    tab_a.with_spare
FROM temp_fleet_providerequipmentrequirementdetail tab_a
LEFT JOIN fleet_equipmentclass tab_b
    ON tab_a.equipment = tab_b.name
LEFT JOIN organization_organization tab_c
    ON tab_a.contractor = tab_c.name
LEFT JOIN fleet_providerequipmentrequirement tab_d
    ON tab_a.year = tab_d.year
        AND tab_c.id = tab_d.contractor_id

