SELECT
    a.date,
    a.type,
    b.name
FROM local_calendar_holiday a,
    local_calendar_holidayevent b
WHERE a.event_id = b.id
ORDER BY a.date, b.name
