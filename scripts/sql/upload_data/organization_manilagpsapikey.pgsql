CREATE TEMPORARY TABLE temp_organization_manilagpsapikey
(
    key character varying(60),
    organization character varying(40)
);

\copy temp_organization_manilagpsapikey FROM 'data/organization_manilagpsapikey.csv' DELIMITER ',' CSV;

INSERT INTO organization_manilagpsapikey (
    key, owner_id
)
SELECT a.key, b.id
FROM temp_organization_manilagpsapikey a,
    organization_organization b
WHERE a.organization = b.name

