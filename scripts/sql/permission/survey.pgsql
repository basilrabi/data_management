GRANT reader TO survey;

GRANT CREATE ON SCHEMA staging TO survey;

GRANT INSERT ON TABLE location_clusterlayout TO survey;
GRANT INSERT ON TABLE location_stockpile     TO survey;

GRANT UPDATE (depth)          ON TABLE inventory_block          TO survey;
GRANT UPDATE                  ON TABLE location_clusterlayout   TO survey;
GRANT UPDATE (geom)           ON TABLE location_drillhole       TO survey;
GRANT UPDATE (x)              ON TABLE location_drillhole       TO survey;
GRANT UPDATE (y)              ON TABLE location_drillhole       TO survey;
GRANT UPDATE (z)              ON TABLE location_drillhole       TO survey;
GRANT UPDATE (z_present)      ON TABLE location_drillhole       TO survey;
GRANT UPDATE (geom)           ON TABLE location_roadarea        TO survey;
GRANT UPDATE                  ON TABLE location_stockpile       TO survey;
GRANT UPDATE (excavated_date) ON TABLE sampling_drillcoresample TO survey;

GRANT SELECT ON SEQUENCE location_clusterlayout_id_seq TO survey;
GRANT SELECT ON SEQUENCE location_stockpile_id_seq     TO survey;

GRANT USAGE  ON SEQUENCE location_clusterlayout_id_seq TO survey;
GRANT USAGE  ON SEQUENCE location_stockpile_id_seq     TO survey;
