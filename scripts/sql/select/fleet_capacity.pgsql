SELECT
    tab_a.value,
    tab_b.name
FROM fleet_capacity tab_a,
    custom_unitofmeasure tab_b
WHERE tab_a.unit_of_measure_id = tab_b.id
ORDER BY tab_b.name, tab_a.value

