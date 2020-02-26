-- gradecontrol
GRANT USAGE ON SCHEMA area TO gradecontrol;
GRANT SELECT ON ALL TABLES IN SCHEMA area TO gradecontrol;
GRANT UPDATE (geom) ON TABLE area.road TO gradecontrol;
GRANT SELECT ON TABLE inventory_block TO gradecontrol;
GRANT SELECT ON TABLE location_cluster TO gradecontrol;
GRANT UPDATE (excavated, cluster_id) ON TABLE inventory_block TO gradecontrol;
GRANT UPDATE (excavated, distance_from_road) ON TABLE location_cluster TO gradecontrol;

-- survey
GRANT USAGE ON SCHEMA area TO survey;
GRANT SELECT ON ALL TABLES IN SCHEMA area TO survey;
GRANT UPDATE (geom) ON TABLE area.road TO survey;
GRANT SELECT ON TABLE location_cluster TO survey;
GRANT UPDATE (with_layout) ON TABLE location_cluster TO survey;
