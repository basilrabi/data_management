CREATE OR REPLACE FUNCTION shipment_name_html(shipment text)
RETURNS text AS
$BODY$
DECLARE shipment_name text;
BEGIN
    CASE
        WHEN shipment ~ '^[0-9]+$' THEN shipment_name = shipment::text
            || '<sup>'
            || RIGHT(TO_CHAR(shipment::integer, '9999th'), 2)
            || '</sup>';
        ELSE shipment_name = shipment;
    END CASE;
    RETURN shipment_name;
END;
$BODY$ LANGUAGE plpgsql;
