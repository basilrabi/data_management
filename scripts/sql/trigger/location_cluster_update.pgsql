CREATE OR REPLACE FUNCTION update_location_cluster_excavated()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the depth field of a clustered block, the
 * cluster is flagged as excavated if all blocks are already excavated.
 */
BEGIN
    IF (NEW.cluster_id IS NOT NULL) THEN

        WITH a as (
            SELECT
                CASE
                    WHEN depth IS NULL THEN 1
                    WHEN depth  > 0 THEN 1
                    ELSE 0
                END as assumed_depth
            FROM inventory_block
            WHERE cluster_id = NEW.cluster_id
        ),
        b as (
            SELECT (
                (COUNT(*) - SUM(assumed_depth)) * 100 / COUNT(*)::float8
            )::integer excavation_rate
            FROM a
        )
        UPDATE location_cluster
        SET
            excavated = b.excavation_rate = 100,
            excavation_rate = b.excavation_rate
        FROM b
        WHERE id = NEW.cluster_id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_excavated_update
ON inventory_block;
CREATE TRIGGER location_cluster_excavated_update
AFTER UPDATE ON inventory_block
FOR EACH ROW
WHEN (NEW.depth <> OLD.depth OR
      (NEW.depth IS NOT NULL AND OLD.depth IS NULL) OR
      (NEW.depth IS NULL AND OLD.cluster_id IS NOT NULL))
EXECUTE PROCEDURE update_location_cluster_excavated();

CREATE OR REPLACE FUNCTION update_location_cluster_geometry()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the referred location_cluster in the foreign
 * key column of `inventory_block`, the geom and elevation colummns of
 * location_cluster is updated.
 */
DECLARE
    cluster_geom geometry;
    elevation integer;
    is_multi_elevation boolean;
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
            mode() WITHIN GROUP (ORDER BY z)
        INTO cluster_geom, elevation
        FROM inventory_block
        WHERE cluster_id = NEW.cluster_id;

        IF (
            (SELECT road_id
             FROM location_cluster
             WHERE id = NEW.cluster_id) IS NOT NULL
        ) THEN
            SELECT ST_MakeValid(ST_Buffer(
                location_roadarea.geom,
                location_cluster.distance_from_road
            ))
            INTO road_buffer
            FROM location_cluster INNER JOIN location_roadarea
            ON location_cluster.road_id = location_roadarea.id
            WHERE location_cluster.id = NEW.cluster_id;

            SELECT ST_Multi(ST_MakeValid(ST_Difference(
                cluster_geom,
                ST_MakeValid(road_buffer)
            )))
            INTO cluster_geom;
        END IF;

        UPDATE location_cluster
        SET z = elevation,
            modified = NOW(),
            geom = cluster_geom
        WHERE id = NEW.cluster_id;
    END IF;

    IF (OLD.cluster_id IS NOT NULL) THEN
        SELECT
            ST_Multi(ST_Union(ST_Expand(geom, 5))),
            mode() WITHIN GROUP (ORDER BY z)
        INTO cluster_geom, elevation
        FROM inventory_block
        WHERE cluster_id = OLD.cluster_id;

        IF (
            (SELECT road_id
             FROM location_cluster
             WHERE id = OLD.cluster_id) IS NOT NULL
        ) THEN
            SELECT ST_MakeValid(ST_Buffer(
                location_roadarea.geom,
                location_cluster.distance_from_road
            ))
            INTO road_buffer
            FROM location_cluster INNER JOIN location_roadarea
            ON location_cluster.road_id = location_roadarea.id
            WHERE location_cluster.id = OLD.cluster_id;

            SELECT ST_Multi(ST_MakeValid(ST_Difference(
                cluster_geom,
                ST_MakeValid(road_buffer)
            )))
            INTO cluster_geom;
        END IF;

        UPDATE location_cluster
        SET z = CASE
                    WHEN elevation IS NOT NULL THEN elevation
                    ELSE 0
                END,
            modified = NOW(),
            geom = cluster_geom
        WHERE id = OLD.cluster_id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_geometry_update
ON inventory_block;
CREATE TRIGGER location_cluster_geometry_update
AFTER UPDATE ON inventory_block
FOR EACH ROW
WHEN (NEW.cluster_id <> OLD.cluster_id OR
      (NEW.cluster_id IS NOT NULL AND OLD.cluster_id IS NULL) OR
      (NEW.cluster_id IS NULL AND OLD.cluster_id IS NOT NULL))
EXECUTE PROCEDURE update_location_cluster_geometry();

CREATE OR REPLACE FUNCTION update_location_cluster_geometry_overlay()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the distance_from_road or the road_id column
 * of location_cluster, the geom column is updated.
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

        IF (NEW.road_id IS NOT NULL) THEN
            SELECT ST_MakeValid(ST_Buffer(location_roadarea.geom, NEW.distance_from_road))
            INTO road_buffer
            FROM location_roadarea
            WHERE id = NEW.road_id;

            SELECT ST_Multi(ST_MakeValid(ST_Difference(cluster_geom, ST_MakeValid(road_buffer))))
            INTO cluster_geom;
        END IF;

        UPDATE location_cluster
        SET geom = ST_MakeValid(cluster_geom),
            modified = NOW()
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_geometry_overlay_update
ON location_cluster;
CREATE TRIGGER location_cluster_geometry_overlay_update
AFTER UPDATE OF distance_from_road, road_id ON location_cluster
FOR EACH ROW
WHEN (NEW.distance_from_road <> OLD.distance_from_road OR
      NEW.road_id <> OLD.road_id OR
      (NEW.road_id IS NOT NULL AND OLD.road_id IS NULL) OR
      (NEW.road_id IS NULL AND OLD.road_id IS NOT NULL))
EXECUTE PROCEDURE update_location_cluster_geometry_overlay();

CREATE OR REPLACE FUNCTION update_location_cluster_name()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the ore_class, mine_block and count columns of
 * location_cluster, the column name is updated.
 */
DECLARE
    new_name text;
BEGIN
    IF (NEW.ore_class IS NOT NULL) THEN

        SELECT concat(NEW.ore_class,
                      NEW.count,
                      '-',
                      lpad(NEW.z::text, 3, '0'),
                      '-',
                      substring(NEW.mine_block from '\d+'))
        INTO new_name;

        UPDATE location_cluster
        SET name = new_name
        WHERE id = NEW.id;

        PERFORM insert_dummy_cluster();
    ELSE
        UPDATE location_cluster
        SET name = '111'
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_name_update
ON location_cluster;
CREATE TRIGGER location_cluster_name_update
AFTER UPDATE OF ore_class, mine_block, count ON location_cluster
FOR EACH ROW
WHEN (NEW.ore_class <> OLD.ore_class OR
      (NEW.ore_class IS NOT NULL AND OLD.ore_class IS NULL) OR
      (NEW.ore_class IS NULL AND OLD.ore_class IS NOT NULL) OR
      NEW.mine_block <> OLD.mine_block OR
      (NEW.mine_block IS NOT NULL AND OLD.mine_block IS NULL) OR
      (NEW.mine_block IS NULL AND OLD.mine_block IS NOT NULL) OR
      NEW.count <> OLD.count OR
      (NEW.count IS NOT NULL AND OLD.count IS NULL) OR
      (NEW.count IS NULL AND OLD.count IS NOT NULL))
EXECUTE PROCEDURE update_location_cluster_name();

CREATE OR REPLACE FUNCTION update_location_cluster_property()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the geom column of location_cluster, the
 * columns ni, fe, co, mine_block and ore_class are also updated based on a
 * weighted average property of all the child inventory_block rows. The weight
 * of each row is based on their area of influence that intersects the geom
 * column of location_cluster.
 */
BEGIN
    IF (NEW.geom IS NOT NULL) THEN
        WITH a as (
            SELECT
                ST_Area(
                    ST_Intersection(
                        ST_Expand(inventory_block.geom, 5),
                        ST_MakeValid(NEW.geom)
                    )
                ) area,
                ni,
                fe,
                co,
                CASE
                    WHEN depth IS NULL THEN 1
                    WHEN depth  > 0 THEN 1
                    ELSE 0
                END as assumed_depth
            FROM inventory_block
            WHERE inventory_block.cluster_id = NEW.id
        ),
        b as (
            SELECT SUM(area) total_area,
                   SUM(ni * area) ni_area,
                   SUM(fe * area) fe_area,
                   SUM(co * area) co_area,
                   COUNT(*) block_count,
                   SUM(assumed_depth) available_block
            FROM a
        ),
        c as (
            SELECT name,
                   ST_Area(ST_Intersection(
                       ST_MakeValid(NEW.geom),
                       location_mineblock.geom
                    )) area
            FROM location_mineblock
            WHERE ST_Intersects(ST_MakeValid(NEW.geom), location_mineblock.geom)
        ),
        d as (
            SELECT name, area
            FROM c
            ORDER BY area DESC
            LIMIT 1
        ),
        e as (
            SELECT round((b.ni_area / b.total_area)::numeric, 2) ni,
                   round((b.fe_area / b.total_area)::numeric, 2) fe,
                   round((b.co_area / b.total_area)::numeric, 2) co,
                   d.name mine_block,
                   (
                       (b.block_count - b.available_block) * 100 / b.block_count::float8
                    )::integer excavation_rate
            FROM b, d
        ),
        f as (
            SELECT get_ore_class(ni, fe) ore_class
            FROM e
        ),
        g as (
            SELECT location_cluster.count
            FROM location_cluster, e, f
            WHERE location_cluster.id <> NEW.id AND
                  location_cluster.ore_class = f.ore_class AND
                  substring(location_cluster.mine_block from '\d+') = substring(e.mine_block from '\d+')
        ),
        h as (
            SELECT generate_series(1, max(g.count) + 1, 1) counts
            FROM g
        ),
        i as (
            SELECT min(counts) count
            FROM h
            WHERE counts NOT IN (
                SELECT count
                FROM g
            )
        )
        UPDATE location_cluster
        SET ni = e.ni,
            fe = e.fe,
            co = e.co,
            mine_block = e.mine_block,
            ore_class = f.ore_class,
            count = CASE
                    WHEN i.count IS NULL THEN 1
                    ELSE i.count
                END,
            excavated = e.excavation_rate = 100,
            excavation_rate = e.excavation_rate
        FROM b, e, f, i
        WHERE id = NEW.id;
    ELSE
        UPDATE location_cluster
        SET ni = 0,
            fe = 0,
            co = 0,
            mine_block = NULL,
            ore_class = NULL,
            count = NULL
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_property_update
ON location_cluster;
CREATE TRIGGER location_cluster_property_update
AFTER UPDATE OF geom ON location_cluster
FOR EACH ROW
WHEN (ST_AsText(NEW.geom) <> ST_AsText(OLD.geom) OR
      (NEW.geom IS NOT NULL AND OLD.geom IS NULL) OR
      (NEW.geom IS NULL AND OLD.geom IS NOT NULL))
EXECUTE PROCEDURE update_location_cluster_property();

CREATE OR REPLACE FUNCTION update_location_cluster_property_from_inventory_block_update()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the ni, fe, and co columns of inventory_block,
 * columns ni, fe, co, and ore_class are also updated.
 */
BEGIN
    WITH area_grade AS (
        SELECT
            ST_Area(
                ST_Intersection(
                    ST_Expand(a.geom, 5),
                    b.geom
                )
            ) area,
            a.co,
            a.fe,
            a.ni
        FROM inventory_block a,
            location_cluster b
        WHERE a.cluster_id = NEW.cluster_id
            AND b.id = NEW.cluster_id
    ),
    area_totals AS (
        SELECT
            SUM(co * area) co_area,
            SUM(fe * area) fe_area,
            SUM(ni * area) ni_area,
            SUM(area) total_area
        FROM area_grade
    ),
    average_grade AS (
        SELECT
            round((co_area / total_area)::numeric, 2) co,
            round((fe_area / total_area)::numeric, 2) fe,
            round((ni_area / total_area)::numeric, 2) ni
        FROM area_totals
    )
    UPDATE location_cluster
    SET co = a.co,
        ni = a.ni,
        fe = a.fe,
        ore_class = get_ore_class(a.ni, a.fe)
    FROM average_grade a
    WHERE id = NEW.cluster_id;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_property_update_from_inventory_block_update
ON location_cluster;
CREATE TRIGGER location_cluster_property_update_from_inventory_block_update
AFTER UPDATE OF co, fe, ni ON inventory_block
FOR EACH ROW
WHEN (
    NEW.cluster_id IS NOT NULL
    AND (
        NEW.co <> OLD.co
        OR NEW.fe <> OLD.fe
        OR NEW.ni <> OLD.ni
    )
)
EXECUTE PROCEDURE update_location_cluster_property_from_inventory_block_update();
