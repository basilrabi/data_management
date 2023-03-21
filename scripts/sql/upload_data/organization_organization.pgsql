CREATE TEMPORARY TABLE temp_organization_organization
(
    name character varying(40),
    description text,
    service character varying(30),
    active boolean
);

\copy temp_organization_organization FROM 'data/organization_organization.csv' DELIMITER ',' CSV;

INSERT INTO organization_organization (
    name, description, service, active
)
SELECT name, description, service, active
FROM temp_organization_organization
