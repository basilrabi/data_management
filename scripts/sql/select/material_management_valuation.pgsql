SELECT
    a.name,
    a.description,
    b.code gl
FROM material_management_valuation a
    LEFT JOIN comptrollership_generalledgeraccount b
        ON a.gl_id = b.id
ORDER BY a.name
