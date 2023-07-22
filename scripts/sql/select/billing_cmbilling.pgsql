SELECT
    tab_a.amount,
    tab_a.billing_year,
    tab_a.half,
    tab_a.last_update,
    tab_a.month,
    tab_a.tonnage,
    tab_b.name
FROM billing_cmbilling tab_a
LEFT JOIN organization_organization tab_b
    ON tab_a.contractor_id = tab_b.id
ORDER BY
    tab_a.billing_year,
    tab_a.month,
    tab_a.half,
    tab_b.name
