SELECT
    a.cancel,
    a.date,
    a.transmittal_number,
    a.nature_of_content,
    a.receiving_copy,
    a.recipient,
    (regexp_match(b.uid, '^[a-z]+'))[1] unit_class,
    b.name unit_name
FROM ormm_externalcommunication a
    LEFT JOIN organization_organizationunit b
        ON a.requesting_department_id = b.id
ORDER BY
    RIGHT(a.transmittal_number, 4),
    LEFT(RIGHT(a.transmittal_number, 8), 3)

