CREATE MATERIALIZED VIEW fleet_equipmentidlinginterval AS
WITH cte_a AS (
    SELECT id,
        equipment_id,
        time_stamp ts_begin,
        LEAD (time_stamp) OVER (PARTITION BY equipment_id ORDER BY time_stamp) ts_end,
        idling,
        LEAD (idling) OVER (PARTITION BY equipment_id ORDER BY time_stamp) next_idling
    FROM fleet_equipmentidlingtime
)
SELECT id,
    equipment_id,
    ts_begin,
    ts_end
FROM cte_a
WHERE idling
    AND NOT next_idling

