CREATE UNIQUE INDEX location_loadingequipmentpath_idx ON location_loadingequipmentpath (id);
CREATE INDEX location_loadingequipmentpath_equipment_id ON location_loadingequipmentpath (equipment_id);
CREATE INDEX location_loadingequipmentpath_kph ON location_loadingequipmentpath (kph);
CREATE INDEX location_loadingequipmentpath_ts_interval ON location_loadingequipmentpath (ts_begin, ts_end);
CREATE INDEX location_loadingequipmentpath_gix ON location_loadingequipmentpath USING gist (geom);

