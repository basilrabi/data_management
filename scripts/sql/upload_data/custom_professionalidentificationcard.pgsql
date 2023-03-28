CREATE TEMPORARY TABLE temp_custom_professionalidentificationcard
(
    "number" character varying(8),
    date_registered date,
    date_expiry date,
    username character varying(150),
    name character varying(20)
);

\copy temp_custom_professionalidentificationcard FROM 'data/custom_professionalidentificationcard.csv' DELIMITER ',' CSV;

INSERT INTO custom_professionalidentificationcard (
    "number",
    date_registered,
    date_expiry,
    holder_id,
    profession_id
)
SELECT
    a.number,
    a.date_registered,
    a.date_expiry,
    b.id,
    c.id
FROM temp_custom_professionalidentificationcard a
    LEFT JOIN custom_user b
        ON a.username = b.username
    LEFT JOIN custom_profession c
        ON a.name = c.name
