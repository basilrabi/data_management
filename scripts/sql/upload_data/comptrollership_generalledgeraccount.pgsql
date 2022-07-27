CREATE TEMPORARY TABLE temp_comptrollership_generalledgeraccount
(
    code integer,
    description text
);

\copy temp_comptrollership_generalledgeraccount FROM 'data/comptrollership_generalledgeraccount.csv' DELIMITER ',' CSV;

INSERT INTO comptrollership_generalledgeraccount (code, description)
SELECT code, description
FROM temp_comptrollership_generalledgeraccount
