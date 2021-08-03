CREATE OR REPLACE FUNCTION add_dummy_location_cluster()
RETURNS TRIGGER AS
$BODY$
-- Always maintain a dummy cluster.
BEGIN
    IF NOT EXISTS(
        SELECT *
        FROM location_cluster
        WHERE name = '111'
    ) THEN
        PERFORM insert_dummy_cluster();
    END IF;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_dummy_insert
ON location_cluster;
CREATE TRIGGER location_cluster_dummy_insert
AFTER INSERT ON location_cluster
FOR EACH ROW
WHEN (NEW.name <> '111')
EXECUTE PROCEDURE add_dummy_location_cluster();

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

CREATE OR REPLACE FUNCTION update_location_cluster_geometry_after_block_delete()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the referred location_cluster in the foreign
 * key column of `inventory_block`, the geom and elevation colummns of
 * location_cluster is updated.
 */
DECLARE
    cluster_geom geometry;
    elevation integer;
    road_buffer geometry;
BEGIN
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

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_geometry_update_after_block_delete
ON inventory_block;
CREATE TRIGGER location_cluster_geometry_update_after_block_delete
AFTER DELETE ON inventory_block
FOR EACH ROW
WHEN (OLD.cluster_id IS NOT NULL)
EXECUTE PROCEDURE update_location_cluster_geometry_after_block_delete();

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
DECLARE
    mine_block_final text;
    mine_block_intersected text;
    mine_block_nearest text;
BEGIN
    IF (NEW.geom IS NOT NULL) THEN
        WITH intersected_mine_blocks AS (
            SELECT
                name,
                ST_Area(ST_Intersection(NEW.geom, geom)) area
            FROM location_mineblock
            WHERE ST_Intersects(geom, NEW.geom)
        )
        SELECT name
        INTO mine_block_intersected
        FROM intersected_mine_blocks
        ORDER BY area DESC
        LIMIT 1;

        SELECT name
        INTO mine_block_nearest
        FROM location_mineblock
        ORDER BY geom <-> NEW.geom
        LIMIT 1;

        SELECT COALESCE(mine_block_intersected, mine_block_nearest)
        INTO mine_block_final;

        WITH area_grade as (
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
        area_totals as (
            SELECT SUM(area) total_area,
                   SUM(ni * area) ni_area,
                   SUM(fe * area) fe_area,
                   SUM(co * area) co_area,
                   COUNT(*) block_count,
                   SUM(assumed_depth) available_block
            FROM area_grade
        ),
        average_grade as (
            SELECT
                round((ni_area / total_area)::numeric, 2) ni,
                round((fe_area / total_area)::numeric, 2) fe,
                round((co_area / total_area)::numeric, 2) co,
                (
                    (block_count - available_block) * 100 / block_count::float8
                )::integer excavation_rate
            FROM area_totals
        ),
        ore_class as (
            SELECT get_ore_class(ni, fe) ore_class
            FROM average_grade
        ),
        cluster_count as (
            SELECT a.count
            FROM location_cluster a, ore_class b
            WHERE a.id <> NEW.id
                AND a.ore_class = b.ore_class
                AND SUBSTRING(a.mine_block FROM '\d+') = SUBSTRING(mine_block_final FROM '\d+')
        ),
        cluster_count_options as (
            SELECT generate_series(1, max(a.count) + 1, 1) counts
            FROM cluster_count a
        ),
        cluster_count_final as (
            SELECT min(counts) count
            FROM cluster_count_options
            WHERE counts NOT IN (
                SELECT count
                FROM cluster_count
            )
        )
        UPDATE location_cluster
        SET ni = a.ni,
            fe = a.fe,
            co = a.co,
            mine_block = mine_block_final,
            ore_class = b.ore_class,
            count = CASE
                    WHEN c.count IS NULL THEN 1
                    ELSE c.count
                END,
            excavated = a.excavation_rate = 100,
            excavation_rate = a.excavation_rate
        FROM average_grade a, ore_class b, cluster_count_final c
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
    WITH affected_cluster AS (
        SELECT id, geom, mine_block
        FROM location_cluster
        WHERE id = NEW.cluster_id
    ),
    area_grade AS (
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
        FROM inventory_block a, affected_cluster b
        WHERE a.cluster_id = NEW.cluster_id
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
    ),
    new_class AS (
        SELECT get_ore_class(ni, fe) ore_class
        FROM average_grade
    ),
    count_list AS (
        SELECT count
        FROM location_cluster a,
            new_class b ,
            affected_cluster c
        WHERE a.id <> NEW.cluster_id AND
            a.ore_class = b.ore_class AND
            SUBSTRING(a.mine_block FROM '\d+') = SUBSTRING(c.mine_block FROM '\d+')
    ),
    count_choice AS (
        SELECT GENERATE_SERIES(1, MAX(a.count) + 1) count
        FROM count_list a
    ),
    count_staging AS (
        SELECT MIN(a.count) count
        FROM count_choice a
        WHERE a.count NOT IN  (
            SELECT count
            FROM count_list
        )
    )
    UPDATE location_cluster
    SET co = a.co,
        ni = a.ni,
        fe = a.fe,
        ore_class = b.ore_class,
        count = CASE
            WHEN c.count IS NULL THEN 1
            ELSE c.count
            END
    FROM average_grade a,
        new_class b,
        count_staging c
    WHERE id = NEW.cluster_id;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_property_update_from_inventory_block_update
ON inventory_block;
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
