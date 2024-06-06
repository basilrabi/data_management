CREATE TEMPORARY TABLE temp_fleet_capacity
(
    value numeric(10, 2),
    name character varying (40)
);

\copy temp_fleet_capacity FROM 'data/fleet_capacity.csv' DELIMITER ',' CSV;

INSERT INTO fleet_capacity (
    unit_of_measure_id,
    value
)
SELECT tab_b.id, tab_a.value
FROM temp_fleet_capacity tab_a
    LEFT JOIN custom_unitofmeasure tab_b
        ON tab_a.name = tab_b.name

