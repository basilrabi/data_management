CREATE OR REPLACE PROCEDURE record_log(txt text)
AS
$BODY$
DECLARE created timestamp with time zone;
BEGIN
    SELECT NOW() INTO created;
    INSERT INTO custom_log (created, log)
    VALUES (created, txt);
END;
$BODY$
LANGUAGE plpgsql;
