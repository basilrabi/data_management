SELECT
    tab_a.adjusted_budget,
    tab_a.actual,
    tab_a.budget,
    tab_a.forecast,
    tab_a.month,
    tab_a.remarks,
    tab_a.year,
    tab_b.name,
    tab_c.code
FROM comptrollership_monthlycost tab_a
    LEFT JOIN comptrollership_sapcostcenter tab_b
        ON tab_a.cost_center_id = tab_b.id
    LEFT JOIN comptrollership_generalledgeraccount tab_c
        ON tab_a.gl_id = tab_c.id
ORDER BY
    tab_a.year,
    tab_a.month,
    tab_b.name,
    tab_c.code
