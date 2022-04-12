CREATE TEMPORARY TABLE temp_sampling_approvedshipmentdischargeassay
(
    shipment_name character varying(10),
    approved boolean,
    certificate character varying(100)
);

\copy temp_sampling_approvedshipmentdischargeassay FROM 'data/sampling_approvedshipmentdischargeassay.csv' DELIMITER ',' CSV;

INSERT INTO sampling_approvedshipmentdischargeassay (approved, certificate, assay_id)
SELECT a.approved, a.certificate, assay.id
FROM temp_sampling_approvedshipmentdischargeassay a
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
    LEFT JOIN sampling_shipmentdischargeassay assay
        ON assay.shipment_id = s.id;

INSERT INTO sampling_approvedshipmentdischargeassay (approved, assay_id)
SELECT 'f', a.id
FROM sampling_shipmentdischargeassay a
WHERE a.id NOT IN (
    SELECT b.assay_id
    FROM sampling_approvedshipmentdischargeassay b
)
