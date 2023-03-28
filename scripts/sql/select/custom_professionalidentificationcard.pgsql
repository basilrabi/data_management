SELECT
    a.number,
    a.date_registered,
    a.date_expiry,
    b.username,
    c.name
FROM custom_professionalidentificationcard a
    LEFT JOIN custom_user b
        ON a.holder_id = b.id
    LEFT JOIN custom_profession c
        ON a.profession_id = c.id
ORDER BY
    c.name, a.number
