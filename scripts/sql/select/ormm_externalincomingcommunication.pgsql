SELECT
    datetime_received,
    scan,
    sender,
    subject,
    transmittal_number
FROM ormm_externalincomingcommunication
ORDER BY SUBSTRING(transmittal_number, 14, 4),
    SUBSTRING(transmittal_number, 10, 3)

