CREATE MATERIALIZED VIEW location_haulingequipmentpath AS
SELECT tab_a.id,
    tab_a.equipment_id,
    tab_a.time_stamp ts_begin,
    lat_a.time_stamp ts_end,
    (
        ST_DISTANCE(tab_a.geom, lat_a.geom) / 1000
    ) / (
        EXTRACT(
            epoch FROM (lat_a.time_stamp - tab_a.time_stamp)
        ) / 3600
    ) kph,
    ST_MAKELINE(tab_a.geom, lat_a.geom) geom
FROM location_haulingequipment tab_a
LEFT JOIN LATERAL (
    SELECT *
    FROM location_haulingequipment tab_b
    WHERE tab_a.equipment_id = tab_b.equipment_id
        AND tab_a.ts_begin = tab_b.ts_begin
        AND tab_a.ts_end = tab_b.ts_end
        AND tab_a.time_stamp < tab_b.time_stamp
    ORDER BY tab_b.time_stamp ASC
    LIMIT 1
) lat_a ON true
WHERE lat_a.ts_end IS NOT NULL

