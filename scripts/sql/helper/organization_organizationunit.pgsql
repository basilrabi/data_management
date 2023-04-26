WITH tab_division AS (
    SELECT 'division' || id  AS id, name, abbreviation
    FROM organization_division
    WHERE name NOT ILIKE 'ind%'
),
tab_department AS (
    SELECT 'department' || id  AS id, name, abbreviation
    FROM organization_department
    WHERE name NOT ILIKE 'ind%'
),
tab_section AS (
    SELECT 'section' || id  AS id, name, name AS abbreviation
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
)
INSERT INTO organization_organizationunit (uid, name, abbreviation)
SELECT *
FROM tab_orgunits
ORDER BY name;
