CREATE UNIQUE INDEX dash_equipmentusage_idx ON dash_equipmentusage (id);
CREATE INDEX dash_equipmentusage_ts_interval ON dash_equipmentusage (ts_begin, ts_end);

