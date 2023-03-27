SELECT
    name,
    date_drilled,
    local_block,
    local_easting,
    local_northing,
    local_z,
    x,
    y,
    z,
    z_present
FROM location_drillhole
ORDER BY name
