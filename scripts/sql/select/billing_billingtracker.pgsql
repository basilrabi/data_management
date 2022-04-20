SELECT
    ROW_NUMBER() OVER() new_id,
    amount,
    contractor,
    end_date,
    fileup,
    id,
    invoice_number,
    last_update,
    operating_hours,
    purpose,
    specification,
    start_date,
    tonnage
FROM billing_billingtracker
ORDER BY id
