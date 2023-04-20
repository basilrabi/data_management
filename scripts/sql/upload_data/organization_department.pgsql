CREATE TEMPORARY TABLE temp_organization_department
(
    abbreviation character varying(10),
    name character varying(30),
    division character varying(30)
);

\copy temp_organization_department FROM 'data/organization_department.csv' DELIMITER ',' CSV;

INSERT INTO organization_department (abbreviation, name, parent_division_id)
SELECT a.abbreviation, a.name, b.id
FROM temp_organization_department a
    LEFT JOIN organization_division b
        ON a.division = b.name
