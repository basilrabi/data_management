SELECT
    tab_a.year,
    tab_b.name contractor
FROM fleet_providerequipmentrequirement tab_a,
    organization_organization tab_b
WHERE tab_a.contractor_id = tab_b.id
ORDER BY tab_a.year DESC,
    tab_b.name

