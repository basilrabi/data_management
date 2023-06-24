CREATE TEMPORARY TABLE temp_ormm_externalcommunication
(
    cancel boolean,
    date date,
    transmittal_number character varying(13),
    nature_of_content text,
    receiving_copy character varying(100),
    recipient character varying(30),
    unit_class text,
    unit_name character varying(30)
);

\copy temp_ormm_externalcommunication FROM 'data/ormm_externalcommunication.csv' DELIMITER ',' CSV;

INSERT INTO ormm_externalcommunication (
    cancel,
    date,
    transmittal_number,
    nature_of_content,
    receiving_copy,
    recipient,
    requesting_department_id
)
SELECT
    a.cancel,
    a.date,
    a.transmittal_number,
    a.nature_of_content,
    a.receiving_copy,
    a.recipient,
    b.id
FROM temp_ormm_externalcommunication a
    LEFT JOIN organization_organizationunit b
        ON a.unit_class || '%' ILIKE b.uid
            AND a.unit_name = b.name
