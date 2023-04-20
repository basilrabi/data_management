SELECT a.name, b.name
FROM organization_section a
    LEFT JOIN organization_department b
        ON a.parent_department_id = b.id
ORDER BY a.name
