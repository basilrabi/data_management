SELECT
    tab_a.time_stamp,
    ST_AsEWKT(tab_a.geom),
    tab_c.name organization,
    tab_e.name equipment_class,
    tab_b.fleet_number,
    tab_f.username
FROM location_equipmentlocation tab_a
    LEFT JOIN fleet_equipment tab_b
        ON tab_a.equipment_id = tab_b.id
    LEFT JOIN organization_organization tab_c
        ON tab_b.owner_id = tab_c.id
    LEFT JOIN fleet_equipmentmodel tab_d
        ON tab_b.model_id = tab_d.id
    LEFT JOIN fleet_equipmentclass tab_e
        ON tab_d.equipment_class_id = tab_e.id
    LEFT JOIN custom_user tab_f
        ON tab_a.user_id = tab_f.id
ORDER BY
    tab_a.time_stamp
