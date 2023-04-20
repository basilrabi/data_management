SELECT a.abbreviation, a.name, b.name
FROM organization_department a
    LEFT JOIN organization_division b
        ON a.parent_division_id = b.id
ORDER BY a.name
