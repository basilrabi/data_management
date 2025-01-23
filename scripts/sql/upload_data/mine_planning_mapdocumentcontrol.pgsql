CREATE TEMPORARY TABLE temp_mine_planning_mapdocumentcontrol
(
    row_id bigint,
    bench character varying(30),
    date_created date,
    id bigint,
    map_title text,
    map_uploads_img character varying(100),
    map_uploads_zip character varying(100),
    material character varying(3),
    mineblock character varying(30),
    month character varying(9),
    number character varying(3),
    revised_from_id bigint,
    ridge character varying(10),
    week_end character varying(2),
    week_start character varying(2),
    revision integer,
    revision_notes text,
    year_on_map character varying(4),
    map_prefix character varying(40),
    map_type character varying(40),
    company character varying(40),
    creator character varying(40)
);

\copy temp_mine_planning_mapdocumentcontrol FROM 'data/mine_planning_mapdocumentcontrol.csv' DELIMITER ',' CSV;

WITH cte_a AS (
    SELECT
        tab_a.bench,
        tab_a.date_created,
        tab_a.map_title,
        tab_a.map_uploads_img,
        tab_a.map_uploads_zip,
        tab_a.material,
        tab_a.mineblock,
        tab_a.month,
        tab_a.number,
        tab_a.ridge,
        tab_a.week_end,
        tab_a.week_start,
        tab_a.revision,
        tab_a.revision_notes,
        tab_a.year_on_map,
        tab_b.row_id revised_from_id,
        tab_c.id map_type_id,
        tab_d.id map_creator_id,
        tab_e.id company_id
    FROM temp_mine_planning_mapdocumentcontrol tab_a
        LEFT JOIN temp_mine_planning_mapdocumentcontrol tab_b
            ON tab_a.revised_from_id = tab_b.id
        LEFT JOIN mine_planning_maptype tab_c
            ON tab_a.map_prefix = tab_c.map_prefix
                AND tab_a.map_type = tab_c.map_type
        LEFT JOIN mine_planning_mineplanningengineer tab_d
            ON tab_a.creator = tab_d.full_name
        LEFT JOIN organization_organization tab_e
            ON tab_a.company = tab_e.name
)
INSERT INTO mine_planning_mapdocumentcontrol (
    bench,
    company_id,
    date_created,
    map_creator_id,
    map_title,
    map_uploads_img,
    map_uploads_zip,
    map_type_id,
    material,
    mineblock,
    month,
    number,
    revised_from_id,
    ridge,
    week_end,
    week_start,
    revision,
    revision_notes,
    year_on_map
)
SELECT
    bench,
    company_id,
    date_created,
    map_creator_id,
    map_title,
    map_uploads_img,
    map_uploads_zip,
    map_type_id,
    material,
    mineblock,
    month,
    number,
    revised_from_id,
    ridge,
    week_end,
    week_start,
    revision,
    revision_notes,
    year_on_map
FROM cte_a

