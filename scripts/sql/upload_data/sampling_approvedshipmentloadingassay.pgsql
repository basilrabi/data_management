CREATE TEMPORARY TABLE temp_sampling_approvedshipmentloadingassay
(
    shipment_name character varying(10),
    approved boolean,
    certificate character varying(100),
    mgb_receipt character varying(100)
);

\copy temp_sampling_approvedshipmentloadingassay FROM 'data/sampling_approvedshipmentloadingassay.csv' DELIMITER ',' CSV;

INSERT INTO sampling_approvedshipmentloadingassay (
    approved, certificate, mgb_receipt, assay_id
)
SELECT a.approved, a.certificate, a.mgb_receipt, assay.id
FROM temp_sampling_approvedshipmentloadingassay a
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
    LEFT JOIN sampling_shipmentloadingassay assay
        ON assay.shipment_id = s.id;

INSERT INTO sampling_approvedshipmentloadingassay (approved, assay_id)
SELECT 'f', a.id
FROM sampling_shipmentloadingassay a
WHERE a.id NOT IN (
    SELECT b.assay_id
    FROM sampling_approvedshipmentloadingassay b
)
