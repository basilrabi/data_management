SELECT
    EXTRACT(year FROM le.interval_from)::integer AS year,
    EXTRACT(month FROM le.interval_from)::integer AS month,
    shipment.name shipment,
    REPLACE(b.arrival_tmc::text, '+08', '') arrival,
    REPLACE(MIN(c.interval_from)::text, '+08', '') as loading_start,
    REPLACE(le.interval_from::text, '+08', '') as loading_end,
    d.name vessel,
    shipment.target_tonnage target_wmt,
    shipment.spec_moisture target_moisture,
    shipment.spec_ni,
    shipment.spec_fe,
    b.tonnage loading_wmt,
    assay.dmt loading_dmt,
    assay.ni loading_ni,
    assay.fe loading_fe,
    dassay.wmt discharging_wmt,
    dassay.dmt discharging_dmt,
    dassay.ni discharging_ni,
    dassay.fe discharging_fe,
    CASE
        WHEN dassay.wmt IS NOT NULL THEN
            CASE
                WHEN shipment.name LIKE '%-C' THEN b.tonnage
                ELSE dassay.wmt - shipment.boulders_tonnage
            END
        ELSE NULL
    END final_wmt,
    shipment.final_moisture,
    shipment.final_ni,
    shipment.final_fe,
    shipment.base_price,
    shipment.final_price,
    shipment.boulders_tonnage,
    shipment.boulders_processing_cost,
    shipment.boulders_freight_cost,
    shipment.dead_freight,
    shipment.despatch - shipment.demurrage despatch,
    lab.name lab_name,
    buyer.name buyer_name
FROM shipment_shipment shipment
    LEFT JOIN shipment_buyer buyer
        ON buyer.id = shipment.buyer_id
    LEFT JOIN sampling_shipmentloadingassay assay
        ON assay.shipment_id = shipment.id
    LEFT JOIN sampling_shipmentdischargeassay dassay
        ON dassay.shipment_id = shipment.id
    LEFT JOIN sampling_laboratory lab
        ON lab.id = dassay.laboratory_id
    LEFT JOIN shipment_laydaysstatement b
        ON b.shipment_id = shipment.id
    LEFT JOIN shipment_laydaysdetail c
        ON c.laydays_id = b.id
    LEFT JOIN shipment_vessel d
        ON d.id = shipment.vessel_id
    LEFT JOIN LATERAL (
        SELECT interval_from
        FROM shipment_laydaysdetail
        WHERE interval_class = 'end'
            AND laydays_id = b.id
    ) le ON true
WHERE b.completed_loading IS NOT NULL
GROUP BY
    shipment.dead_freight,
    shipment.name,
    shipment.spec_moisture,
    shipment.spec_ni,
    shipment.spec_fe,
    shipment.target_tonnage,
    b.arrival_tmc,
    b.tonnage,
    d.name,
    assay.dmt,
    assay.ni,
    assay.fe,
    dassay.wmt,
    dassay.dmt,
    dassay.ni,
    dassay.fe,
    le.interval_from,
    shipment.final_moisture,
    shipment.final_ni,
    shipment.final_fe,
    shipment.base_price,
    shipment.final_price,
    shipment.boulders_tonnage,
    shipment.boulders_processing_cost,
    shipment.boulders_freight_cost,
    shipment.despatch,
    shipment.demurrage,
    lab.name,
    buyer.name
ORDER BY
    le.interval_from,
    shipment.name,
    b.arrival_tmc
