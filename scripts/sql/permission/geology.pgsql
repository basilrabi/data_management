GRANT reader TO geology;

GRANT CREATE ON SCHEMA staging TO geology;

GRANT UPDATE (z_present)      ON TABLE location_drillhole       TO geology;
GRANT UPDATE (excavated_date) ON TABLE sampling_drillcoresample TO geology;
