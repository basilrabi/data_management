CREATE TEMPORARY TABLE temp_material_management_legacygoodsreceivednote
(
    reference_number character varying(10),
    transaction_date date,
    entry_date date,
    material character varying(40),
    purchase_order character varying(8),
    vendor character varying(40),
    invoice_number text,
    invoice_amount float8,
    quantity float8,
    purchase_order_price float8,
    discount float8,
    net_price float8,
    total_price float8
);

\copy temp_material_management_legacygoodsreceivednote FROM 'data/material_management_legacygoodsreceivednote.csv' DELIMITER ',' CSV;

INSERT INTO material_management_legacygoodsreceivednote (
    reference_number,
    transaction_date,
    entry_date,
    purchase_order,
    invoice_number,
    invoice_amount,
    quantity,
    purchase_order_price,
    discount,
    net_price,
    total_price,
    material_id,
    vendor_id
)
SELECT
    a.reference_number,
    a.transaction_date,
    a.entry_date,
    a.purchase_order,
    a.invoice_number,
    a.invoice_amount,
    a.quantity,
    a.purchase_order_price,
    a.discount,
    a.net_price,
    a.total_price,
    b.id,
    c.id
FROM temp_material_management_legacygoodsreceivednote a
    LEFT JOIN material_management_legacymaterial b
        ON a.material = b.name
    LEFT JOIN material_management_legacyvendor c
        ON a.vendor = c.name
