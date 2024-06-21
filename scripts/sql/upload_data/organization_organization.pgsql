CREATE TEMPORARY TABLE temp_organization_organization
(
    active boolean,
    description text,
    name character varying (40),
    resource_code character varying (1),
    service character varying (30),
    warehouse_code character varying (3)
);

\copy temp_organization_organization FROM 'data/organization_organization.csv' DELIMITER ',' CSV;

INSERT INTO organization_organization (
    active,
    description,
    name,
    resource_code,
    service,
    warehouse_code
)
SELECT
    active,
    description,
    name,
    resource_code,
    service,
    warehouse_code
FROM temp_organization_organization

