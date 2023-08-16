CREATE MATERIALIZED VIEW location_loadingequipment AS
WITH loading_equipment AS (
    SELECT tab_a.equipment_id,
        tab_a.time_stamp ts_begin,
        lat_a.time_stamp ts_end
    FROM fleet_equipmentignitionstatus tab_a
    LEFT JOIN fleet_equipment tab_b
        ON tab_a.equipment_id = tab_b.id
    LEFT JOIN fleet_equipmentclass tab_c
        ON tab_b.equipment_class_id = tab_c.id
    LEFT JOIN LATERAL (
        SELECT *
        FROM fleet_equipmentignitionstatus tab_b
        WHERE tab_a.equipment_id = tab_b.equipment_id
            AND NOT tab_b.ignition
            AND tab_b.time_stamp > tab_a.time_stamp
        ORDER BY tab_b.time_stamp
        LIMIT 1
    ) lat_a ON true
    WHERE tab_a.ignition
        AND tab_c.name in ('MW', 'MX', 'TX', 'WL', 'WX')
)
SELECT loading_equipment.*,
    tab_a.id,
    tab_a.time_stamp,
    ST_TRANSFORM(tab_a.geom, 3125) geom
FROM loading_equipment,
    location_equipmentlocation tab_a
WHERE loading_equipment.equipment_id = tab_a.equipment_id
    AND tab_a.time_stamp >= loading_equipment.ts_begin
    AND tab_a.time_stamp <= loading_equipment.ts_end

