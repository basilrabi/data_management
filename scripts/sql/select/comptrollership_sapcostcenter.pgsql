SELECT
    a.description,
    a.long_name,
    a.name,
    a.remarks,
    b.name profit_center
FROM comptrollership_sapcostcenter a
LEFT JOIN comptrollership_profitcenter b
    ON a.profit_center_id = b.id
ORDER BY a.name
