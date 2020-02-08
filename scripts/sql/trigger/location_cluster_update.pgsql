CREATE OR REPLACE FUNCTION update_location_cluster()
RETURNS trigger AS
$BODY$
BEGIN
    WITH new_cluster as (
        SELECT
            ST_Multi(ST_Union(ST_Expand(geom, 5))) geom,
	        mode() WITHIN GROUP (ORDER BY z) z,
	        string_agg(distinct substring(name, 1, 5), ':') mine_block,
	        round(avg(ni::numeric), 2) ni,
	        round(avg(fe::numeric), 2) fe,
	        round(avg(co::numeric), 2) co
        FROM inventory_block
        WHERE
            cluster_id IS NOT NULL AND
            cluster_id = NEW.cluster_id
    )
    UPDATE location_cluster
    SET
        z = new_cluster.z::integer,
        geom = new_cluster.geom,
        mine_block = new_cluster.mine_block,
        ni = new_cluster.ni::numeric,
        fe = new_cluster.fe::numeric,
        co = new_cluster.co::numeric,
        ore_class = get_ore_class(new_cluster.ni::numeric)
    FROM new_cluster
    WHERE id = NEW.cluster_id;

    WITH old_cluster as (
        SELECT
            ST_Multi(ST_Union(ST_Expand(geom, 5))) geom,
	        mode() WITHIN GROUP (ORDER BY z) z,
	        string_agg(distinct substring(name, 1, 5), ':') mine_block,
	        round(avg(ni::numeric), 2) ni,
	        round(avg(fe::numeric), 2) fe,
	        round(avg(co::numeric), 2) co
        FROM inventory_block
        WHERE
            cluster_id IS NOT NULL AND
            cluster_id = OLD.cluster_id
    )
    UPDATE location_cluster
    SET
        z = old_cluster.z::integer,
        geom = old_cluster.geom,
        mine_block = old_cluster.mine_block,
        ni = old_cluster.ni::numeric,
        fe = old_cluster.fe::numeric,
        co = old_cluster.co::numeric,
        ore_class = get_ore_class(old_cluster.ni::numeric)
    FROM old_cluster
    WHERE id = OLD.cluster_id;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS location_cluster_update
ON inventory_block;
CREATE TRIGGER location_cluster_update
AFTER UPDATE ON inventory_block
FOR EACH ROW EXECUTE PROCEDURE update_location_cluster();
