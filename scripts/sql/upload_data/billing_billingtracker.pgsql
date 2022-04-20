CREATE TEMPORARY TABLE temp_billing_billingaddon
(
    billing_id bigint,
    notes_received text,
    notes_sent text,
    received_by timestamp with time zone,
    received_from character varying(32),
    sent_by timestamp with time zone,
    sent_to character varying(32)
);

CREATE TEMPORARY TABLE temp_billing_billingtracker
(
    new_id bigint,
    amount double precision,
    contractor character varying(32),
    end_date date,
    fileup character varying(100),
    id bigint,
    invoice_number character varying(32),
    last_update timestamp with time zone,
    operating_hours double precision,
    purpose character varying(32),
    specification character varying(50),
    start_date date,
    tonnage double precision
);

\copy temp_billing_billingaddon FROM 'data/billing_billingaddon.csv' DELIMITER ',' CSV;
\copy temp_billing_billingtracker FROM 'data/billing_billingtracker.csv' DELIMITER ',' CSV;

INSERT INTO billing_billingtracker (
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
)
SELECT
    amount,
    contractor,
    end_date,
    fileup,
    new_id,
    invoice_number,
    last_update,
    operating_hours,
    purpose,
    specification,
    start_date,
    tonnage
FROM temp_billing_billingtracker
ORDER BY new_id;

INSERT INTO billing_billingaddon (
    billing_id,
    notes_received,
    notes_sent,
    received_by,
    received_from,
    sent_by,
    sent_to
)
SELECT
    b.new_id,
    a.notes_received,
    a.notes_sent,
    a.received_by,
    a.received_from,
    a.sent_by,
    a.sent_to
FROM temp_billing_billingaddon a
    LEFT JOIN temp_billing_billingtracker b
        ON a.billing_id = b.id;
