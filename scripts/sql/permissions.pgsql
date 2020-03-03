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
