GRANT reader TO gradecontrol;

GRANT CREATE SCHEMA staging TO gradecontrol;

GRANT INSERT ON TABLE location_cluster   TO gradecontrol;
GRANT INSERT ON TABLE location_stockpile TO gradecontrol;

GRANT UPDATE (cluster_id)         ON TABLE inventory_block    TO gradecontrol;
GRANT UPDATE (date_scheduled)     ON TABLE location_cluster   TO gradecontrol;
GRANT UPDATE (distance_from_road) ON TABLE location_cluster   TO gradecontrol;
GRANT UPDATE (dumping_area_id)    ON TABLE location_cluster   TO gradecontrol;
GRANT UPDATE (name)               ON TABLE location_cluster   TO gradecontrol;
GRANT UPDATE (road_id)            ON TABLE location_cluster   TO gradecontrol;
GRANT UPDATE                      ON TABLE location_stockpile TO gradecontrol;

GRANT SELECT ON SEQUENCE location_stockpile_id_seq TO gradecontrol;

GRANT USAGE  ON SEQUENCE location_stockpile_id_seq TO gradecontrol;
