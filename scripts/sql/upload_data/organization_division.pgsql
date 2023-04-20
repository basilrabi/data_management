CREATE TEMPORARY TABLE temp_organization_division
(
    abbreviation character varying(10),
    name character varying(30)
);

\copy temp_organization_division FROM 'data/organization_division.csv' DELIMITER ',' CSV;

INSERT INTO organization_division (abbreviation, name)
SELECT abbreviation, name
FROM temp_organization_division
