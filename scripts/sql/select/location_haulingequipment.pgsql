CREATE MATERIALIZED VIEW location_haulingequipment AS
WITH hauling_equipment AS (
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
        AND tab_c.name in ('AD', 'DT', 'GT', 'MD')
)
SELECT ROW_NUMBER() OVER() AS id,
    hauling_equipment.*,
    tab_a.time_stamp,
    tab_a.geom
FROM hauling_equipment
LEFT JOIN location_equipmentlocation tab_a
    ON hauling_equipment.equipment_id = tab_a.equipment_id
        AND tab_a.time_stamp >= hauling_equipment.ts_begin
        AND tab_a.time_stamp <= hauling_equipment.ts_end

