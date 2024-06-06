CREATE TEMPORARY TABLE temp_comptrollership_costcenterconversion
(
    row_id bigint,
    id bigint,
    operation_code smallint,
    with_contract boolean,
    with_inhouse boolean,
    with_rental boolean,
    old_cost_center character varying(40),
    sap_cost_center character varying(40),
    activity_category character varying(40),
    activity_code character varying(40),
    operation_head character varying(40)
);

\copy temp_comptrollership_costcenterconversion FROM 'data/comptrollership_costcenterconversion.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_costcenterconversion (
    activity_category_id,
    activity_code_id,
    old_cost_center_id,
    operation_code,
    operation_head_id,
    sap_cost_center_id,
    with_contract,
    with_inhouse,
    with_rental
)
SELECT
    tab_b.id,
    tab_c.id,
    tab_d.id,
    tab_a.operation_code,
    tab_e.id,
    tab_f.id,
    tab_a.with_contract,
    tab_a.with_inhouse,
    tab_a.with_rental
FROM temp_comptrollership_costcenterconversion tab_a
    LEFT JOIN comptrollership_activitycategory tab_b
        ON tab_a.activity_category = tab_b.name
    LEFT JOIN comptrollership_activitycode tab_c
        ON tab_a.activity_code = tab_c.name
    LEFT JOIN comptrollership_costcenter tab_d
        ON tab_a.old_cost_center = tab_d.name
    LEFT JOIN comptrollership_operationhead tab_e
        ON tab_a.operation_head = tab_e.name
    LEFT JOIN comptrollership_sapcostcenter tab_f
        ON tab_a.sap_cost_center = tab_f.name

