CREATE TEMPORARY TABLE temp_ormm_externalincomingcommunication
(
    datetime_received timestamp with time zone,
    scan character varying(100),
    sender character varying(99),
    subject text,
    transmittal_number character varying(20)
);

\copy temp_ormm_externalincomingcommunication FROM 'data/ormm_externalincomingcommunication.csv' DELIMITER ',' CSV;

INSERT INTO ormm_externalincomingcommunication (
    datetime_received,
    scan,
    sender,
    subject,
    transmittal_number
)
SELECT
    datetime_received,
    scan,
    sender,
    subject,
    transmittal_number
FROM temp_ormm_externalincomingcommunication

