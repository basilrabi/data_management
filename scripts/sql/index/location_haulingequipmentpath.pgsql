CREATE UNIQUE INDEX location_haulingequipmentpath_idx ON location_haulingequipmentpath (id);
CREATE INDEX location_haulingequipmentpath_equipment_id ON location_haulingequipmentpath (equipment_id);
CREATE INDEX location_haulingequipmentpath_ts_begin ON location_haulingequipmentpath (ts_begin);
CREATE INDEX location_haulingequipmentpath_ts_end ON location_haulingequipmentpath (ts_end);
CREATE INDEX location_haulingequipmentpath_gix ON location_haulingequipmentpath USING gist (geom);

