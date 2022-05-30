CREATE TEMPORARY TABLE temp_local_calendar_holidayevent
(
    name character varying(40),
    description text
);

\copy temp_local_calendar_holidayevent FROM 'data/local_calendar_holidayevent.csv' DELIMITER ',' CSV;

INSERT INTO local_calendar_holidayevent (name, description)
SELECT name, description
FROM temp_local_calendar_holidayevent
