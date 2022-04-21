SELECT
    a.name,
    a.description,
    b.name equipment_class,
    c.name manufacturer
FROM fleet_equipmentmodel a
    LEFT JOIN fleet_equipmentclass b
        ON a.equipment_class_id = b.id
    LEFT JOIN fleet_equipmentmanufacturer c
        ON a.manufacturer_id = c.id
ORDER BY a.name
