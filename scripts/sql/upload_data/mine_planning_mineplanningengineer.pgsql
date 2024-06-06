CREATE TEMPORARY TABLE temp_mine_planning_mineplanningengineer
(
    full_name character varying(40)
);

\copy temp_mine_planning_mineplanningengineer FROM 'data/mine_planning_mineplanningengineer.csv' DELIMITER ',' CSV;

INSERT INTO mine_planning_mineplanningengineer (full_name)
SELECT full_name
FROM temp_mine_planning_mineplanningengineer

