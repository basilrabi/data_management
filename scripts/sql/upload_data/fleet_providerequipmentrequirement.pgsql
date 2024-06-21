CREATE TEMPORARY TABLE temp_fleet_providerequipmentrequirement
(
    year smallint,
    contractor character varying (40)
);

\copy temp_fleet_providerequipmentrequirement FROM 'data/fleet_providerequipmentrequirement.csv' DELIMITER ',' CSV;

INSERT INTO fleet_providerequipmentrequirement (
    contractor_id,
    year
)
SELECT
    tab_b.id,
    tab_a.year
FROM temp_fleet_providerequipmentrequirement tab_a,
    organization_organization tab_b
WHERE tab_a.contractor = tab_b.name

