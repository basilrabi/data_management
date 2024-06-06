SELECT
    a.description,
    a.name,
    b.name material
FROM comptrollership_costcenter a
    LEFT JOIN comptrollership_material b
        ON a.material_id = b.id
ORDER BY a.name

