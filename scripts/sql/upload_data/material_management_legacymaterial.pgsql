CREATE TEMPORARY TABLE temp_material_management_legacymaterial
(
    name character varying(40),
    description text,
    item_type character varying(40)
);

\copy temp_material_management_legacymaterial FROM 'data/material_management_legacymaterial.csv' DELIMITER ',' CSV;

INSERT INTO material_management_legacymaterial (
    name, description, item_type_id
)
SELECT a.name, a.description, b.id
FROM temp_material_management_legacymaterial a
    LEFT JOIN material_management_legacyitemtype b
        ON a.item_type = b.name
