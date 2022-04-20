SELECT
    billing_id,
    notes_received,
    notes_sent,
    received_by,
    received_from,
    sent_by,
    sent_to
FROM billing_billingaddon
ORDER BY id
