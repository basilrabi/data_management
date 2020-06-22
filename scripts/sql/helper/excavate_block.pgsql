/* Update inventory_block.depth using a Polygon Z table
 * `topo_schema`.`topo_table`.
 */
CREATE OR REPLACE FUNCTION excavate_inventory_block(topo_schema text,
                                                    topo_table text)
RETURNS integer AS
$BODY$
DECLARE i integer;
BEGIN
    EXECUTE format(
        '   WITH a as ('
        '       SELECT'
        '           block.id,'
        '           ST_Z('
        '               ST_3DIntersection('
        '                   ST_Extrude(block.geom, 0, 0, 600),'
        '                   topo.geom'
        '               )'
        '           ) - (block.z - 1.5) depth'
        '       FROM inventory_block block'
        '           LEFT JOIN %I.%I topo'
        '               ON ST_Intersects(block.geom, topo.geom)'
        '   )'
        '   UPDATE inventory_block'
        '   SET depth = a.depth'
        '   FROM a'
        '   WHERE inventory_block.id = a.id'
        '       AND (a.depth < inventory_block.depth'
        '           OR inventory_block.depth IS NULL)',
        topo_schema,
        topo_table
    );
    GET DIAGNOSTICS i = ROW_COUNT;
    RETURN i;
END;
$BODY$ LANGUAGE plpgsql;
