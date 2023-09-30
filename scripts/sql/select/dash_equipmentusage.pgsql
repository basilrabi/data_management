CREATE MATERIALIZED VIEW dash_equipmentusage AS
WITH cte_a AS (
    SELECT  equipment_id,
        DATE_TRUNC('day', min(ts_begin)) + INTERVAL '6 hours' ts_begin,
        DATE_TRUNC('day', max(ts_end)) + INTERVAL '6 hours' ts_end
    FROM fleet_equipmentignitioninterval
    GROUP BY equipment_id
),
cte_b AS (
    SELECT equipment_id,
        gs time_stamp,
        'shift' as event
    FROM cte_a,
        GENERATE_SERIES(ts_begin, ts_end, interval '12 hours') gs
),
cte_c AS (
    SELECT *
    FROM cte_b
    UNION
    SELECT equipment_id,
        time_stamp,
        CASE
            WHEN idling then 'idling start'
            ELSE 'idling end'
        END AS event
    FROM fleet_equipmentidlingtime
    UNION
    SELECT equipment_id,
        time_stamp,
        CASE
            WHEN ignition then 'ignition start'
            ELSE 'ignition end'
        END as event
    FROM fleet_equipmentignitionstatus
),
cte_d AS (
    SELECT equipment_id,
        time_stamp,
        ARRAY_AGG(event) event,
        COUNT(*) n
    FROM cte_c
    GROUP BY equipment_id, time_stamp
    ORDER BY equipment_id, time_stamp, event
),
cte_e AS (
    SELECT equipment_id,
        time_stamp ts_begin,
        event,
        LEAD (event) OVER (PARTITION BY equipment_id ORDER BY time_stamp) next_event,
        LEAD (time_stamp) OVER (PARTITION BY equipment_id ORDER BY time_stamp) ts_end
    FROM cte_d
)
SELECT cte_e.*,
    fleet_equipment.fleet_number,
    fleet_equipmentclass.name equipment_class,
    CASE
        WHEN event = ARRAY['shift'] AND next_event = ARRAY['idling start'] THEN 'ignition'
        WHEN event = ARRAY['shift'] AND next_event = ARRAY['ignition end'] THEN 'ignition'
        WHEN event = ARRAY['shift'] AND next_event = ARRAY['shift'] THEN 'standby'
        WHEN event = ARRAY['shift'] AND next_event @> ARRAY['idling end'] THEN 'idling'
        WHEN event = ARRAY['shift'] AND next_event @> ARRAY['ignition start'] THEN 'standby'
        WHEN event = ARRAY['idling end'] THEN 'ignition'
        WHEN event = ARRAY['ignition start'] THEN 'ignition'
        WHEN event @> ARRAY['idling end'] AND next_event @> ARRAY['idling start'] THEN 'ignition'
        WHEN event @> ARRAY['idling end'] AND next_event @> ARRAY['ignition end'] THEN 'ignition'
        WHEN event @> ARRAY['idling start'] THEN 'idling'
        WHEN event @> ARRAY['ignition end'] THEN 'standby'
        WHEN event @> ARRAY['ignition start', 'shift'] AND next_event @> ARRAY['ignition end'] THEN 'ignition'
        ELSE NULL
    END utilization,
    CASE
        WHEN fleet_equipment.date_acquired IS NOT NULL AND organization_organization.name = 'TMC'
            THEN 'TMC-' || fleet_equipmentclass.name || RIGHT(EXTRACT('year' FROM fleet_equipment.date_acquired)::text, 2) || '-' || LPAD(fleet_equipment.fleet_number::text, 3, 0::text)
        WHEN organization_organization.name = 'TMC'
            THEN 'TMC-' || fleet_equipmentclass.name || '00-' || LPAD(fleet_equipment.fleet_number::text, 3, 0::text)
        ELSE NULL
    END name,
    ROW_NUMBER() OVER () AS id
FROM cte_e,
    fleet_equipment,
    fleet_equipmentclass,
    organization_organization
WHERE cte_e.ts_end IS NOT NULL
    AND cte_e.equipment_id = fleet_equipment.id
    AND fleet_equipment.equipment_class_id = fleet_equipmentclass.id
    AND fleet_equipment.owner_id = organization_organization.id

