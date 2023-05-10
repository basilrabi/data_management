GRANT gradecontrol TO planning;
GRANT reader       TO planning;
GRANT survey       TO planning;

GRANT DELETE ON TABLE location_slice TO planning;

GRANT INSERT ON TABLE inventory_block TO planning;
GRANT INSERT ON TABLE location_slice  TO planning;

GRANT UPDATE (co)                      ON TABLE inventory_block          TO planning;
GRANT UPDATE (depth)                   ON TABLE inventory_block          TO planning;
GRANT UPDATE (fe)                      ON TABLE inventory_block          TO planning;
GRANT UPDATE (ni)                      ON TABLE inventory_block          TO planning;
GRANT UPDATE (planned_excavation_date) ON TABLE inventory_block          TO planning;
GRANT UPDATE (z_present)               ON TABLE location_drillhole       TO planning;
GRANT UPDATE (excavated_date)          ON TABLE sampling_drillcoresample TO planning;

GRANT SELECT ON SEQUENCE location_slice_id_seq TO planning;

GRANT USAGE  ON SEQUENCE location_slice_id_seq TO planning;
