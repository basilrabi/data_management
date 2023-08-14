CREATE UNIQUE INDEX location_loadingequipment_idx ON location_loadingequipment (id);
CREATE INDEX location_loadingequipment_ts_begin ON location_loadingequipment (ts_begin);
CREATE INDEX location_loadingequipment_ts_end ON location_loadingequipment (ts_end);
CREATE INDEX location_loadingequipment_gix ON location_loadingequipment USING gist (geom);

