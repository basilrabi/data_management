SELECT
    core.date_received_for_preparation,
    core.date_prepared,
    core.date_received_for_analysis,
    core.date_analyzed,
    core.al,
    core.al2o3,
    core.arsenic,
    core.c,
    core.cao,
    core.co,
    core.cr,
    core.cr2o3,
    core.fe,
    core.k,
    core.mg,
    core.mgo,
    core.mn,
    core.ni,
    core.p,
    core.pb,
    core.s,
    core.sc,
    core.si,
    core.sio2,
    core.zn,
    core.ignition_loss,
    core.moisture,
    hole.name,
    core.interval_from,
    core.interval_to,
    litho.name,
    litho_mod.name,
    core.description,
    core.excavated_date
FROM sampling_drillcoresample as core
    LEFT JOIN location_drillhole as hole
        ON core.drill_hole_id = hole.id
    LEFT JOIN sampling_lithology as litho
        ON core.lithology_id = litho.id
    LEFT JOIN sampling_lithology as litho_mod
        ON core.lithology_modified_id = litho_mod.id
ORDER BY hole.name, core.interval_from
