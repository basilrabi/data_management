SELECT
    a.number,
    a.spaceless_number,
    b.username
FROM custom_mobilenumber a
    LEFT JOIN custom_user b
        ON a.user_id = b.id
ORDER BY
    a.spaceless_number
