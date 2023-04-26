SELECT
    a.reference_number,
    a.transaction_date,
    a.entry_date,
    b.name material_name,
    a.purchase_order,
    c.name vendor_name,
    a.invoice_number,
    a.invoice_amount,
    a.quantity,
    a.purchase_order_price,
    a.discount,
    a.net_price,
    a.total_price
FROM material_management_legacygoodsreceivednote a
    LEFT JOIN material_management_legacymaterial b
        ON a.material_id = b.id
    LEFT JOIN material_management_legacyvendor c
        ON a.vendor_id = c.id
ORDER BY
    a.transaction_date,
    a.entry_date,
    a.reference_number,
    a.purchase_order,
    b.name,
    c.name,
    a.invoice_number,
    a.quantity
