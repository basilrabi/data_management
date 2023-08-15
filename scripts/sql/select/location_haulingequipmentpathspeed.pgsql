CREATE MATERIALIZED VIEW location_haulingequipmentpathspeed AS
SELECT id, (
    ST_LENGTH(geom) / 1000
) / (
    EXTRACT(epoch FROM (ts_end - ts_begin)) / 3600
) kph
FROM location_haulingequipmentpath

