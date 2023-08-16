CREATE UNIQUE INDEX location_loadingequipment_idx ON location_loadingequipment (id);
CREATE INDEX location_loadingequipment_equipment_id ON location_loadingequipment (equipment_id);
CREATE INDEX location_loadingequipment_timestamp ON location_loadingequipment (time_stamp);
CREATE INDEX location_loadingequipment_ts_interval ON location_loadingequipment (ts_begin, ts_end);
CREATE INDEX location_loadingequipment_gix ON location_loadingequipment USING gist (geom);

