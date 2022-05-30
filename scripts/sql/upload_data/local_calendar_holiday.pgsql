CREATE TEMPORARY TABLE temp_local_calendar_holiday
(
    date date,
    type character varying(2),
    name character varying(40)
);

\copy temp_local_calendar_holiday FROM 'data/local_calendar_holiday.csv' DELIMITER ',' CSV;

INSERT INTO local_calendar_holiday (date, type, event_id)
SELECT a.date, a.type, b.id
FROM temp_local_calendar_holiday a
    LEFT JOIN local_calendar_holidayevent b
        ON a.name = b.name
