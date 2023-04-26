SELECT
    a.order_number,
    a.transaction_date,
    a.entry_date,
    a.order_type,
    b.name material_name,
    a.cost_center,
    a.equipment,
    a.quantity,
    a.unit_cost,
    a.total_cost
FROM material_management_legacygoodsissuance a
    LEFT JOIN material_management_legacymaterial b
        ON a.material_id = b.id
ORDER BY
    a.transaction_date,
    a.entry_date,
    a.order_number,
    a.order_type,
    b.name,
    a.cost_center,
    a.equipment,
    a.quantity,
    a.total_cost
