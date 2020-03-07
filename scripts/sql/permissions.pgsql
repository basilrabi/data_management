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
GRANT SELECT ON TABLE location_cluster TO gradecontrol;
GRANT SELECT ON TABLE location_roadarea TO gradecontrol;
GRANT UPDATE (cluster_id, excavated) ON TABLE inventory_block TO gradecontrol;
GRANT UPDATE (
    date_scheduled,
    distance_from_road,
    excavated,
    name,
    road_id
) ON TABLE location_cluster TO gradecontrol;

-- survey
GRANT CREATE, USAGE ON SCHEMA staging TO survey;
GRANT SELECT ON TABLE location_cluster TO survey;
GRANT SELECT ON TABLE location_roadarea TO gradecontrol;
GRANT UPDATE (geom) ON TABLE location_roadarea TO survey;
GRANT UPDATE (with_layout) ON TABLE location_cluster TO survey;
