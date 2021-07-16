GRANT reader TO survey;

GRANT CREATE ON SCHEMA staging TO survey;

GRANT INSERT ON TABLE location_clusterlayout TO survey;
GRANT INSERT ON TABLE location_stockpile     TO survey;

GRANT UPDATE        ON TABLE location_clusterlayout TO survey;
GRANT UPDATE (geom) ON TABLE location_roadarea      TO survey;
GRANT UPDATE        ON TABLE location_stockpile     TO survey;

GRANT SELECT ON SEQUENCE location_clusterlayout_id_seq TO survey;
GRANT SELECT ON SEQUENCE location_stockpile_id_seq     TO survey;

GRANT USAGE  ON SEQUENCE location_clusterlayout_id_seq TO survey;
GRANT USAGE  ON SEQUENCE location_stockpile_id_seq     TO survey;
