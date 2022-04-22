CREATE TEMPORARY TABLE temp_custom_mobilenumber
(
    "number" character varying(128),
    spaceless_number character varying(20),
    username character varying(150)
);

\copy temp_custom_mobilenumber FROM 'data/custom_mobilenumber.csv' DELIMITER ',' CSV;

INSERT INTO custom_mobilenumber (
    "number",
    spaceless_number,
    user_id
)
SELECT
    a.number,
    a.spaceless_number,
    b.id
FROM temp_custom_mobilenumber a
    LEFT JOIN custom_user b
        ON a.username = b.username
