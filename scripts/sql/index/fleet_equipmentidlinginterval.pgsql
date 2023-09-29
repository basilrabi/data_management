CREATE UNIQUE INDEX fleet_equipmentidlinginterval_idx ON fleet_equipmentidlinginterval (id);
CREATE INDEX fleet_equipmentidlinginterval_equipment_id ON fleet_equipmentidlinginterval (equipment_id);
CREATE INDEX fleet_equipmentdlinginterval_ts_interval ON fleet_equipmentidlinginterval (ts_begin, ts_end);

