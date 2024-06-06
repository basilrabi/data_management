SELECT a.key, b.name organization
FROM organization_manilagpsapikey a,
    organization_organization b
WHERE a.owner_id = b.id
ORDER BY b.name,
    a.key

