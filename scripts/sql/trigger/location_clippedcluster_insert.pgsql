CREATE OR REPLACE FUNCTION insert_location_clippedcluster()
RETURNS trigger AS
$BODY$
-- Whenever a new cluster is inserted, also insert a new clipped cluster.
DECLARE
    cluster_geom geometry;
    crest_geom geometry;
    co double precision;
    fe double precision;
    ni double precision;
BEGIN
    IF NEW.geom IS NULL OR ST_IsEmpty(NEW.geom) THEN
        INSERT INTO location_clippedcluster (
            cluster_id,
            co,
            date_scheduled,
            excavated,
            fe,
            geom,
            latest_layout_date,
            mine_block,
            modified,
            name,
            ni,
            ore_class,
            z
        )
        VALUES (
            NEW.id,
            NEW.co,
            NEW.date_scheduled,
            NEW.excavated,
            NEW.fe,
            NEW.geom,
            NEW.latest_layout_date,
            NEW.mine_block,
            NEW.modified,
            NEW.name,
            NEW.ni,
            NEW.ore_class,
            NEW.z
        );
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
            cluster_geom := ST_Intersection(NEW.geom, slice_geom);
        END IF;

        WITH aa AS (
            SELECT
                ST_Area(
                    ST_Intersection(ST_Expand(geom, 5), cluster_geom)
                ) area,
                co,
                fe,
                ni
            FROM inventory_block
            WHERE cluster_id = NEW.id
        ),
        bb AS (
            SELECT
                SUM(area) total_area,
                SUM(co * area) co_area,
                SUM(fe * area) fe_area,
                SUM(ni * area) ni_area
        )
        SELECT
            round((co_area / total_area)::numeric, 2),
            round((fe_area / total_area)::numeric, 2),
            round((ni_area / total_area)::numeric, 2)
        INTO co, fe, ni
        FROM bb;

        INSERT INTO location_clippedcluster (
            cluster_id,
            co,
            date_scheduled,
            excavated,
            fe,
            geom,
            latest_layout_date,
            mine_block,
            modified,
            name,
            ni,
            ore_class,
            z
        )
        VALUES (
            NEW.id,
            co,
            NEW.date_scheduled,
            NEW.excavated,
            fe,
            cluster_geom,
            NEW.latest_layout_date,
            NEW.mine_block,
            NEW.modified,
            NEW.name,
            ni,
            get_ore_class(ni, fe),
            NEW.z
        );
    END IF;

    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_clippedcluster_insert
ON location_cluster;
CREATE TRIGGER location_clippedcluster_insert
AFTER INSERT ON location_cluster
FOR EACH ROW
EXECUTE PROCEDURE insert_location_clippedcluster();
