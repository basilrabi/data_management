CREATE MATERIALIZED VIEW organization_organizationunit AS
WITH tab_division AS (
    SELECT 'division' type, name, abbreviation
    FROM organization_division
    WHERE name NOT ILIKE 'ind%'
),
tab_department AS (
    SELECT 'department' type, name, abbreviation
    FROM organization_department
    WHERE name NOT ILIKE 'ind%'
),
tab_section AS (
    SELECT 'section' type, name, name AS abbreviation
    FROM organization_section
    WHERE name NOT ILIKE 'ind%'
),
tab_orgunits AS (
    SELECT *
    FROM tab_division
    UNION
    SELECT *
    FROM tab_department
    UNION
    SELECT *
    FROM tab_section
),
tab_ordered AS (
    SELECT *
    FROM tab_orgunits
    ORDER BY name
)
SELECT *, row_number() over() AS id
FROM tab_ordered
