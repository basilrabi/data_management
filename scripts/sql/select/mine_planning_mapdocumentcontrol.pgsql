SELECT
    ROW_NUMBER() OVER() row_id,
    a.bench,
    a.date_created,
    a.id,
    a.map_uploads_img,
    a.map_uploads_zip,
    a.material,
    a.mineblock,
    a.month,
    a.number,
    a.revised_from_id,
    a.ridge,
    a.week_end,
    a.week_start,
    a.revision,
    a.revision_notes,
    a.year_on_map,
    b.map_prefix,
    b.map_type,
    c.name company,
    d.full_name creator
FROM mine_planning_mapdocumentcontrol a
    LEFT JOIN mine_planning_maptype b
        ON a.map_type_id = b.id
    LEFT JOIN organization_organization c
        ON a.company_id = c.id
    LEFT JOIN mine_planning_mineplanningengineer d
        ON a.map_creator_id = d.id
ORDER BY a.id

