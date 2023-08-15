CREATE UNIQUE INDEX location_loadingequipmentpath_idx ON location_loadingequipmentpath (id);
CREATE INDEX location_loadingequipmentpath_equipment_id ON location_loadingequipmentpath (equipment_id);
CREATE INDEX location_loadingequipmentpath_ts_begin ON location_loadingequipmentpath (ts_begin);
CREATE INDEX location_loadingequipmentpath_ts_end ON location_loadingequipmentpath (ts_end);
CREATE INDEX location_loadingequipmentpath_gix ON location_loadingequipmentpath USING gist (geom);

