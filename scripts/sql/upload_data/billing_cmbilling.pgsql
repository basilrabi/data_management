CREATE TEMPORARY TABLE temp_billing_cmbilling
(
    amount double precision,
    billing_year character varying(4),
    half character varying(3),
    last_update timestamp with time zone,
    month character varying(9),
    tonnage double precision,
    contractor character varying(40)
);

\copy temp_billing_cmbilling FROM 'data/billing_cmbilling.csv' DELIMITER ',' CSV;

INSERT INTO billing_cmbilling (
    amount,
    billing_year,
    half,
    last_update,
    month,
    tonnage,
    contractor_id
)
SELECT
    tab_a.amount,
    tab_a.billing_year,
    tab_a.half,
    tab_a.last_update,
    tab_a.month,
    tab_a.tonnage,
    tab_b.id
FROM temp_billing_cmbilling tab_a
    LEFT JOIN organization_organization tab_b
        ON tab_a.contractor = tab_b.name;

