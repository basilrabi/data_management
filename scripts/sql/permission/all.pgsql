-- geology
GRANT CREATE, USAGE ON SCHEMA staging TO geology;
GRANT USAGE ON SCHEMA topography TO geology;
GRANT SELECT ON ALL TABLES IN SCHEMA topography TO geology;
GRANT SELECT ON TABLE location_drillhole TO geology;
GRANT UPDATE (z_present) ON TABLE location_drillhole TO geology;
GRANT SELECT ON TABLE location_mineblock TO geology;
GRANT SELECT ON TABLE sampling_drillcoresample TO geology;
GRANT UPDATE (excavated_date) ON TABLE sampling_drillcoresample TO geology;

-- gradecontrol
GRANT CREATE, USAGE ON SCHEMA staging TO gradecontrol;
GRANT SELECT ON TABLE inventory_block TO gradecontrol;
GRANT SELECT ON TABLE location_slice TO gradecontrol;
GRANT INSERT, SELECT ON TABLE location_cluster TO gradecontrol;
GRANT SELECT ON TABLE location_mineblock TO gradecontrol;
GRANT SELECT ON TABLE location_roadarea TO gradecontrol;
GRANT UPDATE (cluster_id) ON TABLE inventory_block TO gradecontrol;
GRANT UPDATE (
    date_scheduled,
    distance_from_road,
    name,
    road_id
) ON TABLE location_cluster TO gradecontrol;

-- survey
GRANT CREATE, USAGE ON SCHEMA staging TO survey;
GRANT SELECT ON TABLE location_cluster TO survey;
GRANT SELECT ON TABLE location_drillhole TO survey;
GRANT SELECT ON TABLE location_mineblock TO survey;
GRANT SELECT ON TABLE location_roadarea TO survey;
GRANT SELECT ON TABLE location_slice TO survey;
GRANT SELECT ON TABLE sampling_drillcoresample TO survey;
GRANT UPDATE (geom) ON TABLE location_roadarea TO survey;
GRANT UPDATE (layout_date) ON TABLE location_cluster TO survey;

-- reader
GRANT USAGE ON SCHEMA staging TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA staging TO reader;

-- planning
GRANT gradecontrol TO planning;
GRANT survey TO planning;
GRANT INSERT ON TABLE location_slice TO planning;
GRANT UPDATE (depth)          ON TABLE inventory_block TO planning;
GRANT UPDATE (z_present)      ON TABLE location_drillhole TO planning;
GRANT UPDATE (layer, z)       ON TABLE location_slice TO planning;
GRANT UPDATE (excavated_date) ON TABLE sampling_drillcoresample TO planning;
GRANT USAGE, SELECT ON SEQUENCE location_slice_id_seq TO planning;
