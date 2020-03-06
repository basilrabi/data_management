SELECT
    core.date_received_for_preparation,
    core.date_prepared,
    core.date_received_for_analysis,
    core.date_analyzed,
    core.al,
    core.c,
    core.co,
    core.cr,
    core.fe,
    core.mg,
    core.ni,
    core.sc,
    core.si,
    core.moisture,
    hole.name,
    core.interval_from,
    core.interval_to,
    litho.name,
    core.description,
    core.excavated_date
FROM sampling_drillcoresample as core
    LEFT JOIN location_drillhole as hole
        ON core.drill_hole_id = hole.id
    LEFT JOIN sampling_lithology as litho
        ON core.lithology_id = litho.id
ORDER BY hole.name, core.interval_from
