SELECT a.name, a.description, b.name item_type
FROM material_management_legacymaterial a
    LEFT JOIN material_management_legacyitemtype b
        ON a.item_type_id = b.id
ORDER BY a.name
