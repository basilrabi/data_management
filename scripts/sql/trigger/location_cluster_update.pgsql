CREATE OR REPLACE FUNCTION update_location_cluster_geometry()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the referred location_cluster in the foreign
 * key column of `inventory_block`, the geom colummn of location_cluster is
 * updated.
 */
DECLARE
    cluster_geom geometry;
    elevation integer;
    is_multi_elevation boolean;
    new_mine_block text;
    road_buffer geometry;
BEGIN
    IF (NEW.cluster_id IS NOT NULL) THEN

        SELECT mod(avg(z), mode() WITHIN GROUP (ORDER BY z)) > 0
        INTO is_multi_elevation
        FROM inventory_block
        WHERE cluster_id = NEW.cluster_id;

        IF is_multi_elevation THEN
            RAISE EXCEPTION 'Blocks are not at the same elevation.';
        END IF;

        SELECT
            ST_Multi(ST_Union(ST_Expand(geom, 5))),
            mode() WITHIN GROUP (ORDER BY z),
            string_agg(distinct substring(name, 1, 5), ':')
        INTO cluster_geom, elevation, new_mine_block
        FROM inventory_block
        WHERE cluster_id = NEW.cluster_id;

        IF (
            (SELECT distance_from_road
             FROM location_cluster
             WHERE id = NEW.cluster_id) IS NOT NULL
        ) THEN
            SELECT ST_Buffer(area.road.geom, location_cluster.distance_from_road)
            INTO road_buffer
            FROM area.road, location_cluster
            WHERE location_cluster.id = NEW.cluster_id;

            SELECT ST_Difference(cluster_geom, road_buffer)
            INTO cluster_geom;
        END IF;

        UPDATE location_cluster
        SET z = elevation,
            geom = cluster_geom,
            mine_block = new_mine_block
        WHERE id = NEW.cluster_id;
    END IF;

    IF (OLD.cluster_id IS NOT NULL) THEN
        SELECT
            ST_Multi(ST_Union(ST_Expand(geom, 5))),
            mode() WITHIN GROUP (ORDER BY z),
            string_agg(distinct substring(name, 1, 5), ':')
        INTO cluster_geom, elevation, new_mine_block
        FROM inventory_block
        WHERE cluster_id = OLD.cluster_id;

        IF (
            (SELECT distance_from_road
             FROM location_cluster
             WHERE id = OLD.cluster_id) IS NOT NULL
        ) THEN
            SELECT ST_Buffer(area.road.geom, location_cluster.distance_from_road)
            INTO road_buffer
            FROM area.road, location_cluster
            WHERE location_cluster.id = OLD.cluster_id;

            SELECT ST_Difference(cluster_geom, road_buffer)
            INTO cluster_geom;
        END IF;

        UPDATE location_cluster
        SET z = elevation,
            geom = cluster_geom,
            mine_block = new_mine_block
        WHERE id = OLD.cluster_id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_geometry_update
ON inventory_block;
CREATE TRIGGER location_cluster_geometry_update
AFTER UPDATE ON inventory_block
FOR EACH ROW EXECUTE PROCEDURE update_location_cluster_geometry();

CREATE OR REPLACE FUNCTION update_location_cluster_geometry_overlay()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the distance_from_road column of
 * location_cluster, the geom column is updated.
 */
DECLARE
    cluster_geom geometry;
    has_child boolean;
    road_buffer geometry;
BEGIN
    SELECT count(*) > 0
    INTO has_child
    FROM inventory_block
    WHERE cluster_id = NEW.id;

    IF has_child THEN
        SELECT ST_Multi(ST_Union(ST_Expand(geom, 5)))
        INTO cluster_geom
        FROM inventory_block
        WHERE cluster_id = NEW.id;

        IF (NEW.distance_from_road IS NOT NULL) THEN
            SELECT ST_Buffer(area.road.geom, NEW.distance_from_road)
            INTO road_buffer
            FROM area.road;

            SELECT ST_Difference(cluster_geom, road_buffer)
            INTO cluster_geom;
        END IF;

        UPDATE location_cluster
        SET geom = cluster_geom
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_geometry_overlay_update
ON location_cluster;
CREATE TRIGGER location_cluster_geometry_overlay_update
AFTER UPDATE OF distance_from_road ON location_cluster
FOR EACH ROW EXECUTE PROCEDURE update_location_cluster_geometry_overlay();

CREATE OR REPLACE FUNCTION update_location_cluster_property()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the geom column of location_cluster, the
 * columns ni, fe, and co are also updated based on a weighted average property
 * of all the child inventory_block rows. The weight of each row is based on
 * their area of influence that intersects the geom column of location_cluster.
 */
BEGIN
    IF (NEW.geom IS NOT NULL) THEN
        WITH a as (
            SELECT
                ST_Area(
                    ST_Intersection(
                        ST_Expand(inventory_block.geom, 5), NEW.geom
                    )
                ) area, ni, fe, co
            FROM inventory_block
            WHERE inventory_block.cluster_id = NEW.id
        ),
        b as (
            SELECT SUM(area) total_area,
                   SUM(ni * area) ni_area,
                   SUM(fe * area) fe_area,
                   SUM(co * area) co_area
            FROM a
        )
        UPDATE location_cluster
        SET ni = ni_area / total_area,
            fe = fe_area / total_area,
            co = co_area / total_area
        FROM b
        WHERE id = NEW.id;
    ELSE
        UPDATE location_cluster
        SET ni = 0,
            fe = 0,
            co = 0
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_property_update
ON location_cluster;
CREATE TRIGGER location_cluster_property_update
AFTER UPDATE OF geom ON location_cluster
FOR EACH ROW EXECUTE PROCEDURE update_location_cluster_property();
