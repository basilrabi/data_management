CREATE UNIQUE INDEX location_haulingequipment_idx ON location_haulingequipment (id);
CREATE INDEX location_haulingequipment_ts_begin ON location_haulingequipment (ts_begin);
CREATE INDEX location_haulingequipment_ts_end ON location_haulingequipment (ts_end);
CREATE INDEX location_haulingequipment_gix ON location_haulingequipment USING gist (geom);

