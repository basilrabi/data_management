CREATE TEMPORARY TABLE temp_sampling_shipmentloadinglotassay
(
    lot smallint,
    ni numeric(6,4),
    moisture numeric(6,4),
    wmt numeric(8,3),
    shipment_name character varying(10)
);

\copy temp_sampling_shipmentloadinglotassay FROM 'data/sampling_shipmentloadinglotassay.csv' DELIMITER ',' CSV;

INSERT INTO sampling_shipmentloadinglotassay (
    lot, ni, moisture, wmt, shipment_assay_id
)
SELECT a.lot, a.ni, a.moisture, a.wmt, assay.id
FROM temp_sampling_shipmentloadinglotassay a
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
    LEFT JOIN sampling_shipmentloadingassay assay
        ON assay.shipment_id = s.id
