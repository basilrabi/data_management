WITH qa as (
	SELECT
		lmb.name mine_block,
		EXTRACT(YEAR FROM ib.planned_excavation_date) as year,
		EXTRACT(MONTH FROM ib.planned_excavation_date) as month,
		get_ore_class(ib.ni::numeric, ib.fe::numeric) as ore_class,
		ib.depth < 0 excavated,
		lc.date_scheduled IS NOT NULL clustered
	FROM inventory_block ib
		LEFT JOIN location_mineblock lmb
			ON ST_Intersects(ib.geom, lmb.geom)
		LEFT JOIN location_cluster lc
			ON ib.cluster_id = lc.id
	WHERE ib.planned_excavation_date IS NOT NULL
),
qb as (
	SELECT
		qa.year,
		qa.month,
		qa.mine_block,
		qa.ore_class,
		count(*) planned_blocks,
		sum(qa.clustered::integer) planned_blocks_clustered,
		sum(qa.excavated::integer) planned_blocks_excavated
	FROM qa
	GROUP BY
		qa.year,
		qa.month,
		qa.mine_block,
		qa.ore_class
	ORDER BY
		qa.year,
		qa.month,
		qa.mine_block,
		qa.ore_class
),
qc as (
	SELECT
		lmb.name mine_block,
		EXTRACT(YEAR FROM lc.date_scheduled) as year,
		EXTRACT(MONTH FROM lc.date_scheduled) as month,
		get_ore_class(ib.ni::numeric, ib.fe::numeric) as ore_class,
		ib.depth < 0 excavated
	FROM inventory_block ib
		INNER JOIN location_cluster lc
			ON ib.cluster_id = lc.id
		LEFT JOIN location_mineblock lmb
			ON ST_Intersects(ib.geom, lmb.geom)
	WHERE ib.planned_excavation_date IS NULL
		AND lc.date_scheduled IS NOT NULL
),
qd as (
	SELECT
		year,
		month,
		mine_block,
		ore_class,
		count(*) unplanned_blocks_clustered,
		sum(excavated::integer) unplanned_blocks_clustered_and_excavated
	FROM qc
	GROUP BY year, month, mine_block, ore_class
),
qe as (
	SELECT
		CASE
			WHEN qb.year IS NOT NULL THEN qb.year
			ELSE qd.year
		END as year,
		CASE
			WHEN qb.month IS NOT NULL THEN qb.month
			ELSE qd.month
		END as month,
		CASE
			WHEN qb.ore_class IS NOT NULL THEN qb.ore_class
			ELSE qd.ore_class
		END as ore_class,
		CASE
			WHEN qb.mine_block IS NOT NULL THEN qb.mine_block
			ELSE qd.mine_block
		END as mine_block,
		planned_blocks,
		planned_blocks_clustered,
		planned_blocks_excavated,
		unplanned_blocks_clustered,
		unplanned_blocks_clustered_and_excavated
	FROM qb FULL JOIN qd
		ON qb.year = qd.year
			AND qb.month = qd.month
			AND qb.mine_block = qd.mine_block
			AND qb.ore_class = qd.ore_class
)
SELECT
	year,
	month,
	ore_class,
	mine_block,
	CASE
		WHEN planned_blocks IS NULL THEN 0
		ELSE planned_blocks
	END planned_blocks,
	CASE
		WHEN planned_blocks_clustered IS NULL THEN 0
		ELSE planned_blocks_clustered
	END planned_blocks_clustered,
	CASE
		WHEN planned_blocks_excavated IS NULL THEN 0
		ELSE planned_blocks_excavated
	END planned_blocks_excavated,
	CASE
		WHEN unplanned_blocks_clustered IS NULL THEN 0
		ELSE unplanned_blocks_clustered
	END unplanned_blocks_clustered,
	CASE
		WHEN unplanned_blocks_clustered_and_excavated IS NULL THEN 0
		ELSE unplanned_blocks_clustered_and_excavated
	END unplanned_blocks_clustered_and_excavated
FROM qe
ORDER BY qe.year, qe.month, qe.ore_class, qe.mine_block
