CREATE MATERIALIZED VIEW fleet_equipmentignitioninterval AS
WITH cte_a AS (
    SELECT id,
        equipment_id,
        time_stamp ts_begin,
        LEAD (time_stamp) OVER (PARTITION BY equipment_id ORDER BY time_stamp) ts_end,
        ignition,
        LEAD (ignition) OVER (PARTITION BY equipment_id ORDER BY time_stamp) next_ignition
    FROM fleet_equipmentignitionstatus
)
SELECT id,
    equipment_id,
    ts_begin,
    ts_end
FROM cte_a
WHERE ignition
    AND NOT next_ignition

