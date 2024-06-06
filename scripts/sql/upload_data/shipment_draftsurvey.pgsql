CREATE TEMPORARY TABLE temp_shipment_draftsurvey
(
    images_in_pdf character varying (100),
    mgb_receipt character varying (100),
    shipment character varying (10),
    video character varying (100)
);

\copy temp_shipment_draftsurvey FROM 'data/shipment_draftsurvey.csv' DELIMITER ',' CSV;

INSERT INTO shipment_draftsurvey (
    images_in_pdf,
    mgb_receipt,
    shipment_id,
    video
)
SELECT
    a.images_in_pdf,
    a.mgb_receipt,
    b.id,
    a.video
FROM temp_shipment_draftsurvey a,
    shipment_shipment b
WHERE a.shipment = b.name

