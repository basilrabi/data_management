SELECT
    b.name,
    c.name
FROM
    comptrollership_costcenterconversion a,
    comptrollership_costcenter b,
    comptrollership_sapcostcenter c
WHERE
    a.old_cost_center_id = b.id and
    a.sap_cost_center_id = c.id
ORDER BY
    c.name,
    b.name
