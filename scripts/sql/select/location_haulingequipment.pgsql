CREATE MATERIALIZED VIEW location_haulingequipment AS
SELECT tab_a.id,
    tab_a.time_stamp,
    tab_b.equipment_id,
    tab_b.ts_begin,
    tab_b.ts_end,
    ST_TRANSFORM(tab_a.geom, 3125) geom
FROM location_equipmentlocation tab_a,
    fleet_equipmentignitioninterval tab_b,
    fleet_equipment tab_c,
    fleet_equipmentclass tab_d
WHERE tab_a.equipment_id = tab_b.equipment_id
    AND tab_a.time_stamp >= tab_b.ts_begin
    AND tab_a.time_stamp <= tab_b.ts_end
    AND tab_b.equipment_id = tab_c.id
    AND tab_c.equipment_class_id = tab_d.id
    AND tab_d.name IN ('AD', 'DT', 'GT', 'MD')

