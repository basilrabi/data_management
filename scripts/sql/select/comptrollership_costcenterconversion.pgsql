WITH cte_a AS (
    SELECT
        tab_a.id,
        tab_a.operation_code,
        tab_a.with_contract,
        tab_a.with_inhouse,
        tab_a.with_rental,
        tab_b.name old_cost_center,
        tab_c.name sap_cost_center,
        tab_d.name activity_category,
        tab_e.name activity_code,
        tab_f.name operation_head
    FROM comptrollership_costcenterconversion tab_a
        LEFT JOIN comptrollership_costcenter tab_b
            ON tab_a.old_cost_center_id = tab_b.id
        LEFT JOIN comptrollership_sapcostcenter tab_c
            ON tab_a.sap_cost_center_id = tab_c.id
        LEFT JOIN comptrollership_activitycategory tab_d
            ON tab_a.activity_category_id = tab_d.id
        LEFT JOIN comptrollership_activitycode tab_e
            ON tab_a.activity_code_id = tab_e.id
        LEFT JOIN comptrollership_operationhead tab_f
            ON tab_a.operation_head_id = tab_f.id
    ORDER BY
        tab_c.name,
        tab_b.name
)
SELECT ROW_NUMBER() OVER() row_id, *
FROM cte_a

