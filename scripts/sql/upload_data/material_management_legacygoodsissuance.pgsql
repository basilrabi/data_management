CREATE TEMPORARY TABLE temp_material_management_legacygoodsissuance
(
    order_number character varying(10),
    transaction_date date,
    entry_date date,
    order_type character varying(10),
    material character varying(40),
    cost_center character varying(8),
    equipment text,
    quantity float8,
    unit_cost float8,
    total_cost float8
);

\copy temp_material_management_legacygoodsissuance FROM 'data/material_management_legacygoodsissuance.csv' DELIMITER ',' CSV;

INSERT INTO material_management_legacygoodsissuance (
    order_number,
    transaction_date,
    entry_date,
    order_type,
    cost_center,
    equipment,
    quantity,
    unit_cost,
    total_cost,
    material_id
)
SELECT
    a.order_number,
    a.transaction_date,
    a.entry_date,
    a.order_type,
    a.cost_center,
    a.equipment,
    a.quantity,
    a.unit_cost,
    a.total_cost,
    b.id
FROM temp_material_management_legacygoodsissuance a
    LEFT JOIN material_management_legacymaterial b
        ON a.material = b.name
