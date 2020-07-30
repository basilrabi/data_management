SELECT
    a.name,
    a.description,
    a.moisture,
    a.ni,
    a.fe
FROM shipment_product a
ORDER BY a.name
