CREATE TEMPORARY TABLE temp_organization_organization
(
    name character varying(40),
    description text
);

\copy temp_organization_organization FROM 'data/organization_organization.csv' DELIMITER ',' CSV;

INSERT INTO organization_organization (name, description)
SELECT name, description
FROM temp_organization_organization
