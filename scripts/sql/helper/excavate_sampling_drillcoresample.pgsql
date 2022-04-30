-- Set sampling_drillcoresample.excavated date using z_present of a cetain date.
CREATE OR REPLACE FUNCTION excavate_sampling_drillcoresample(topo_date date)
RETURNS integer AS
$BODY$
DECLARE i integer;
BEGIN
    EXECUTE format(
        '   WITH a as ('
        '       SELECT'
        '           core.id,'
        '           CASE'
        '               WHEN dh.z_present IS NOT NULL THEN dh.z_present'
        '               ELSE dh.z'
        '           END as z_present,'
        '           dh.z as z,'
        '           core.interval_to'
        '       FROM location_drillhole dh, sampling_drillcoresample core'
        '       WHERE dh.id = core.drill_hole_id'
        '   ),'
        '   b as ('
        '       SELECT *, (z - z_present) change_elevation'
        '       FROM a'
        '   ),'
        '   c as ('
        '       SELECT *'
        '       FROM b'
        '       WHERE interval_to < change_elevation'
        '   )'
        '   UPDATE sampling_drillcoresample'
        '   SET excavated_date = ''%s'''
        '   FROM c'
        '   WHERE sampling_drillcoresample.id = c.id'
        '       AND sampling_drillcoresample.excavated_date IS NULL',
        topo_date
    );
    GET DIAGNOSTICS i = ROW_COUNT;
    RETURN i;
END;
$BODY$ LANGUAGE plpgsql;
