WITH cte as (
    SELECT MAX(id) id FROM billing_billingtracker
)
SELECT setval('billing_billingtracker_id_seq'::regclass, id)
FROM cte;
