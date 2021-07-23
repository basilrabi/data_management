CREATE OR REPLACE FUNCTION update_location_clippedcluster_geom_from_location_cluster_fields()
RETURNS trigger AS
$BODY$
-- If location_cluster fields are updated, update the other fields of
-- location_clippedcluster too.
BEGIN
    UPDATE location_clippedcluster
    SET date_scheduled = NEW.date_scheduled,
        excavated = NEW.excavated,
        latest_layout_date = NEW.latest_layout_date,
        mine_block = NEW.mine_block,
        modified = NEW.modified,
        name = NEW.name,
        z = NEW.z
    WHERE cluster_id = NEW.id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_update_from_location_cluster_fields
ON location_cluster;
CREATE TRIGGER location_clippedcluster_update_from_location_cluster_fields
AFTER UPDATE OF
    date_scheduled,
    excavated,
    latest_layout_date,
    mine_block,
    modified,
    name,
    z
ON location_cluster
FOR EACH ROW
EXECUTE PROCEDURE update_location_clippedcluster_geom_from_location_cluster_fields();

CREATE OR REPLACE FUNCTION update_location_clippedcluster_geom_from_location_cluster_geom()
RETURNS trigger AS
$BODY$
-- If location_cluster.geom is updated, update location_clippedcluster.geom too.
DECLARE
    cluster_geom geometry;
    crest_geom geometry;
BEGIN
    IF NEW.geom IS NULL OR ST_IsEmpty(NEW.geom) THEN
        UPDATE location_clippedcluster
        SET geom = NEW.geom
        WHERE cluster_id = NEW.id;
    ELSE
        SELECT ST_Union(geom)
        INTO crest_geom
        FROM location_crest
        WHERE z + 3 = NEW.z
            AND ST_Intersects(location_crest.geom, NEW.geom)
            AND ST_GeometryType(
                ST_Intersection(location_crest.geom, NEW.geom)
            ) IN ('ST_Polygon', 'ST_MultiPolygon');

        IF crest_geom IS NULL OR ST_IsEmpty(crest_geom) THEN
            cluster_geom := NEW.geom;
        ELSE
            cluster_geom := ST_Intersection(NEW.geom, crest_geom);
        END IF;

        UPDATE location_clippedcluster
        SET geom = ST_Multi(cluster_geom)
        WHERE cluster_id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_geom_update_from_location_cluster_geom
ON location_cluster;
CREATE TRIGGER location_clippedcluster_geom_update_from_location_cluster_geom
AFTER UPDATE OF geom
ON location_cluster
FOR EACH ROW
EXECUTE PROCEDURE update_location_clippedcluster_geom_from_location_cluster_geom();

CREATE OR REPLACE FUNCTION update_location_clippedcluster_geom_from_location_crest_delete()
RETURNS trigger AS
$BODY$
-- If a crest is deleted, update the affected location_clippedcluster.geom.
BEGIN
    WITH affected AS (
        SELECT id
        FROM location_cluster
        WHERE z - 3 = OLD.z
            AND geom && OLD.geom
            AND (
                ST_Overlaps(geom, OLD.geom)
                    OR ST_Contains(geom, OLD.geom)
                    OR ST_Contains(OLD.geom, geom)
            )
    ),
    crest_overlay AS (
        SELECT
            a.id,
            ST_Union(b.geom) geom
        FROM location_cluster a, location_crest b
        WHERE a.id IN (SELECT id FROM affected)
            AND a.z - 3 = b.z
            AND a.geom && b.geom
            AND (
                ST_Overlaps(a.geom, b.geom)
                    OR ST_Contains(a.geom, b.geom)
                    OR ST_Contains(b.geom, a.geom)
            )
        GROUP BY a.id
    ),
    clipped AS (
        SELECT
            a.id,
            CASE
                WHEN b.geom IS NULL OR ST_IsEmpty(b.geom) THEN a.geom
                ELSE ST_Multi(ST_Intersection(a.geom, b.geom))
            END geom
        FROM location_cluster a
            LEFT JOIN crest_overlay b ON a.id = b.id
        WHERE a.id IN (SELECT id FROM affected)
    )
    UPDATE location_clippedcluster
    SET geom = clipped.geom
    FROM clipped
    WHERE cluster_id = clipped.id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_geom_update_from_location_crest_delete
ON location_crest;
CREATE TRIGGER location_clippedcluster_geom_update_from_location_crest_delete
AFTER DELETE
ON location_crest
FOR EACH ROW
EXECUTE PROCEDURE update_location_clippedcluster_geom_from_location_crest_delete();

CREATE OR REPLACE FUNCTION update_location_clippedcluster_geom_from_location_crest_insert()
RETURNS trigger AS
$BODY$
-- If a crest is inserted, update the affected location_clippedcluster.geom.
BEGIN
    WITH affected AS (
        SELECT id
        FROM location_cluster a
        WHERE z - 3 = NEW.z
            AND ST_Intersects(a.geom, NEW.geom)
            AND ST_GeometryType(
                ST_Intersection(a.geom, NEW.geom)
            ) IN ('ST_Polygon', 'ST_MultiPolygon')
    ),
    crest_overlay AS (
        SELECT
            a.id,
            ST_Union(b.geom) geom
        FROM location_cluster a, location_crest b
        WHERE a.id IN (SELECT id FROM affected)
            AND a.z - 3 = b.z
            AND ST_Intersects(a.geom, b.geom)
            AND ST_GeometryType(
                ST_Intersection(a.geom, b.geom)
            ) IN ('ST_Polygon', 'ST_MultiPolygon')
        GROUP BY a.id
    ),
    clipped AS (
        SELECT
            a.id,
            CASE
                WHEN b.geom IS NULL OR ST_IsEmpty(b.geom) THEN a.geom
                ELSE ST_Multi(ST_Intersection(a.geom, b.geom))
            END geom
        FROM location_cluster a
            LEFT JOIN crest_overlay b ON a.id = b.id
        WHERE a.id IN (SELECT id FROM affected)
    )
    UPDATE location_clippedcluster
    SET geom = clipped.geom
    FROM clipped
    WHERE cluster_id = clipped.id;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_geom_update_from_location_crest_insert
ON location_crest;
CREATE TRIGGER location_clippedcluster_geom_update_from_location_crest_insert
AFTER INSERT
ON location_crest
FOR EACH ROW
EXECUTE PROCEDURE update_location_clippedcluster_geom_from_location_crest_insert();

CREATE OR REPLACE FUNCTION update_location_clippedcluster_property()
RETURNS trigger AS
$BODY$
/* Whenever there is a change in the geom column of location_clippedcluster, the
 * columns ni, fe, co and ore_class are also updated based on a weighted average
 * property of all the spatially overlapped inventory_block. The weight of
 * each row is based on their area of influence that intersects the geom
 * column of location_clippedcluster.
 */
BEGIN
    IF (NEW.geom IS NOT NULL) THEN
        WITH area_grade AS (
            SELECT
                ST_Area(
                    ST_Intersection(
                        ST_Expand(inventory_block.geom, 5),
                        NEW.geom
                    )
                ) area,
                co,
                fe,
                ni
            FROM inventory_block
            WHERE inventory_block.cluster_id = NEW.cluster_id
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
        UPDATE location_clippedcluster
        SET co = a.co,
            ni = a.ni,
            fe = a.fe,
            ore_class = get_ore_class(a.ni, a.fe)
        FROM average_grade a
        WHERE id = NEW.id;
    ELSE
        UPDATE location_clippedcluster
        SET co = 0,
            fe = 0,
            ni = 0,
            ore_class = NULL
        WHERE id = NEW.id;
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_property_update
ON location_cluster;
CREATE TRIGGER location_clippedcluster_property_update
AFTER UPDATE OF geom ON location_clippedcluster
FOR EACH ROW
WHEN (ST_AsText(NEW.geom) <> ST_AsText(OLD.geom) OR
      (NEW.geom IS NOT NULL AND OLD.geom IS NULL) OR
      (NEW.geom IS NULL AND OLD.geom IS NOT NULL))
EXECUTE PROCEDURE update_location_clippedcluster_property();

CREATE OR REPLACE FUNCTION update_location_clippedcluster_property_from_inventory_block_update()
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
            location_clippedcluster b
        WHERE a.cluster_id = NEW.cluster_id
            AND b.cluster_id = NEW.cluster_id
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
    UPDATE location_clippedcluster
    SET co = a.co,
        ni = a.ni,
        fe = a.fe,
        ore_class = get_ore_class(a.ni, a.fe)
    FROM average_grade a
    WHERE cluster_id = NEW.cluster_id;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_property_update_from_inventory_block_update
ON location_cluster;
CREATE TRIGGER location_clippedcluster_property_update_from_inventory_block_update
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
EXECUTE PROCEDURE update_location_clippedcluster_property_from_inventory_block_update();
