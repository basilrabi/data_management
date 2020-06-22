/* Update location_drillhole.z_present using a Polygon Z table
 * `topo_schema`.`topo_table`.
 */
CREATE OR REPLACE FUNCTION update_location_drillhole_z_present(topo_schema text,
                                                               topo_table text)
RETURNS integer AS
$BODY$
DECLARE i integer;
BEGIN
    EXECUTE format(
        '   WITH elev as ('
	    '       SELECT'
        '           dh.id as id,'
        '           ST_Z('
        '               ST_3DIntersection('
        '                   ST_Extrude(dh.geom, 0, 0, 1000),'
        '                   topo.geom'
        '               )'
        '           ) as z_2020'
        '       FROM location_drillhole dh, %I.%I topo'
        '       WHERE ST_Intersects(dh.geom, topo.geom)'
        '   )'
        '   UPDATE location_drillhole'
        '   SET z_present = z_2020'
        '   FROM elev'
        '   WHERE location_drillhole.id = elev.id',
        topo_schema,
        topo_table
    );
    GET DIAGNOSTICS i = ROW_COUNT;
    RETURN i;
END;
$BODY$ LANGUAGE plpgsql;
