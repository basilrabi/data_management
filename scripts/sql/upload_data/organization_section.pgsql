CREATE TEMPORARY TABLE temp_organization_section
(
    name character varying(30),
    department character varying(30)
);

\copy temp_organization_section FROM 'data/organization_section.csv' DELIMITER ',' CSV;

INSERT INTO organization_section (name, parent_department_id)
SELECT a.name, b.id
FROM temp_organization_section a
    LEFT JOIN organization_department b
        ON a.department = b.name
