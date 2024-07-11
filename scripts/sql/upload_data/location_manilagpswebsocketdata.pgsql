CREATE TEMPORARY TABLE temp_location_manilagpswebsocketdata
(
    alt smallint,
    battery_level smallint,
    call_time timestamp with time zone,
    connection_status text,
    heading smallint,
    last_blocked timestamp with time zone,
    last_success timestamp with time zone,
    lat double precision,
    lon double precision,
    movement_status text,
    network_name text,
    signal_level smallint,
    speed smallint,
    tracker_id integer,
    update_battery timestamp with time zone,
    update_gps timestamp with time zone,
    update_gsm timestamp with time zone,
    update_last timestamp with time zone,
    fleet_number smallint,
    equipment_class character varying(40),
    organization character varying(40)
);

\copy temp_location_manilagpswebsocketdata FROM 'data/location_manilagpswebsocketdata.csv' DELIMITER ',' CSV;

INSERT INTO location_manilagpswebsocketdata (
    alt,
    battery_level,
    call_time,
    connection_status,
    equipment_id,
    geom,
    heading,
    last_blocked,
    last_success,
    lat,
    lon,
    movement_status,
    network_name,
    signal_level,
    speed,
    tracker_id,
    update_battery,
    update_gps,
    update_gsm,
    update_last
)
SELECT
    tab_a.alt,
    tab_a.battery_level,
    tab_a.call_time,
    tab_a.connection_status,
    tab_b.id,
    ST_MAKEPOINT(tab_a.lon, tab_a.lat),
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
    tab_a.update_last
FROM temp_location_manilagpswebsocketdata tab_a,
    fleet_equipment tab_b,
    fleet_equipmentclass tab_c,
    organization_organization tab_d
WHERE tab_a.equipment_class = tab_c.name
    AND tab_a.fleet_number = tab_b.fleet_number
    AND tab_a.organization = tab_d.name
    AND tab_b.equipment_class_id = tab_c.id
    AND tab_b.owner_id = tab_d.id

