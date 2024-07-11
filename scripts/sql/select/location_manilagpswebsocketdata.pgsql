SELECT
    tab_a.alt,
    tab_a.battery_level,
    tab_a.call_time,
    tab_a.connection_status,
    tab_a.heading,
    tab_a.last_blocked,
    tab_a.last_success,
    tab_a.lat,
    tab_a.lon,
    tab_a.movement_status,
    tab_a.network_name,
    tab_a.signal_level,
    tab_a.speed,
    tab_a.tracker_id,
    tab_a.update_battery,
    tab_a.update_gps,
    tab_a.update_gsm,
    tab_a.update_last,
    tab_b.fleet_number,
    tab_c.name equipment_class,
    tab_d.name organization
FROM location_manilagpswebsocketdata tab_a,
    fleet_equipment tab_b,
    fleet_equipmentclass tab_c,
    organization_organization tab_d
WHERE tab_a.equipment_id = tab_b.id
    AND tab_b.equipment_class_id = tab_c.id
    AND tab_b.owner_id = tab_d.id
ORDER BY
    tab_d.name,
    tab_c.name,
    tab_b.fleet_number

