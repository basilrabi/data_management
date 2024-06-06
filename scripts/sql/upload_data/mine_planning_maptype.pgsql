CREATE TEMPORARY TABLE temp_mine_planning_maptype
(
    map_prefix character varying(40),
    map_type character varying(40)
);

\copy temp_mine_planning_maptype FROM 'data/mine_planning_maptype.csv' DELIMITER ',' CSV;

INSERT INTO mine_planning_maptype (
    map_prefix,
    map_type
)
SELECT
    map_prefix,
    map_type
FROM temp_mine_planning_maptype

