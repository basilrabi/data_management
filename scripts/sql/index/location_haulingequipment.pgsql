CREATE UNIQUE INDEX location_haulingequipment_idx ON location_haulingequipment (id);
CREATE INDEX location_haulingequipment_equipment_id ON location_haulingequipment (equipment_id);
CREATE INDEX location_haulingequipment_timestamp ON location_haulingequipment (time_stamp);
CREATE INDEX location_haulingequipment_ts_interval ON location_haulingequipment (ts_begin, ts_end);
CREATE INDEX location_haulingequipment_gix ON location_haulingequipment USING gist (geom);

