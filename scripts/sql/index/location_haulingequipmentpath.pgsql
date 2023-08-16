CREATE UNIQUE INDEX location_haulingequipmentpath_idx ON location_haulingequipmentpath (id);
CREATE INDEX location_haulingequipmentpath_equipment_id ON location_haulingequipmentpath (equipment_id);
CREATE INDEX location_haulingequipmentpath_kph ON location_haulingequipmentpath (kph);
CREATE INDEX location_haulingequipmentpath_ts_interval ON location_haulingequipmentpath (ts_begin, ts_end);
CREATE INDEX location_haulingequipmentpath_gix ON location_haulingequipmentpath USING gist (geom);

