CREATE TEMPORARY TABLE temp_sampling_approvedshipmentloadingassay
(
    approved boolean,
    shipment_name character varying(10)
);

\copy temp_sampling_approvedshipmentloadingassay FROM 'data/sampling_approvedshipmentloadingassay.csv' DELIMITER ',' CSV;

INSERT INTO sampling_approvedshipmentloadingassay (approved, assay_id)
SELECT a.approved, assay.id
FROM temp_sampling_approvedshipmentloadingassay a
    LEFT JOIN shipment_shipment s
        ON s.name = a.shipment_name
    LEFT JOIN sampling_shipmentloadingassay assay
        ON assay.shipment_id = s.id
