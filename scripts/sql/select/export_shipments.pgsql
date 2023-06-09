WITH cte AS (
    SELECT
        EXTRACT(year FROM le.interval_from)::integer AS year,
        EXTRACT(month FROM le.interval_from)::integer AS month,
        shipment.name shipment,
        REPLACE(b.arrival_tmc::text, '+08', '') arrival,
        REPLACE(MIN(c.interval_from)::text, '+08', '') as loading_start,
        REPLACE(le.interval_from::text, '+08', '') as loading_end,
        d.name vessel,
        destination.name destination,
        shipment.target_tonnage target_wmt,
        shipment.spec_moisture target_moisture,
        shipment.spec_ni,
        shipment.spec_fe,
        b.tonnage loading_wmt,
        assay.dmt loading_dmt,
        assay.ni loading_ni,
        assay.fe loading_fe,
        assay.mgo loading_mgo,
        assay.sio2 loading_sio2,
        assay.moisture loading_moisture,
        assay.cr loading_cr,
        assay.co loading_co,
        dassay.wmt discharging_wmt,
        dassay.dmt discharging_dmt,
        dassay.ni discharging_ni,
        dassay.fe discharging_fe,
        CASE
            WHEN dassay.mgo IS NOT NULL THEN dassay.mgo
            WHEN dassay.mg IS NOT NULL THEN ROUND(dassay.mg * 1.658259617, 4)
            ELSE NULL
        END discharging_mgo,
        CASE
            WHEN dassay.sio2 IS NOT NULL THEN dassay.sio2
            WHEN dassay.si IS NOT NULL THEN ROUND(dassay.si * 2.139327043, 4)
            ELSE NULL
        END discharging_sio2,
        dassay.moisture discharging_moisture,
        CASE
            WHEN dassay.cr IS NOT NULL THEN dassay.cr
            WHEN dassay.cr2o3 IS NOT NULL THEN ROUND(dassay.cr2o3 / 1.461543699, 4)
            ELSE NULL
        END discharging_cr,
        dassay.co discharging_co,
        CASE
            WHEN dassay.wmt IS NOT NULL THEN
                CASE
                    WHEN shipment.name LIKE '%B' THEN b.tonnage - shipment.boulders_tonnage
                    WHEN shipment.name LIKE '%C' THEN b.tonnage
                    WHEN shipment.name LIKE '%M' THEN dassay.wmt - shipment.boulders_tonnage
                    WHEN shipment.name LIKE '%P' THEN b.tonnage - shipment.boulders_tonnage
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
        buyer.name buyer_name,
        ST_Distance(
            ST_Transform(e.geom, 3125),
            'SRID=3125;POINT(589742 1056033)'::geometry
        ) / 1000 distance_from_wharf
    FROM shipment_shipment shipment
        LEFT JOIN shipment_destination destination
            ON shipment.destination_id = destination.id
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
        LEFT JOIN location_anchorage e
            ON e.laydays_id = b.id
        LEFT JOIN LATERAL (
            SELECT interval_from
            FROM shipment_laydaysdetail
            WHERE interval_class = 'end'
                AND laydays_id = b.id
        ) le ON true
    WHERE b.completed_loading IS NOT NULL
    GROUP BY
        destination.name,
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
        assay.mgo,
        assay.sio2,
        assay.moisture,
        assay.cr,
        assay.co,
        dassay.wmt,
        dassay.dmt,
        dassay.ni,
        dassay.fe,
        dassay.mg,
        dassay.mgo,
        dassay.si,
        dassay.sio2,
        dassay.moisture,
        dassay.cr,
        dassay.cr2o3,
        dassay.co,
        e.geom,
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
)
SELECT
    year,
    month,
    shipment,
    arrival,
    loading_start,
    loading_end,
    vessel,
    target_wmt,
    target_moisture,
    spec_ni,
    spec_fe,
    destination,
    loading_wmt,
    loading_dmt,
    loading_ni,
    loading_fe,
    loading_mgo,
    loading_sio2,
    loading_moisture,
    loading_cr,
    loading_co,
    discharging_wmt,
    discharging_dmt,
    discharging_ni,
    discharging_fe,
    discharging_mgo,
    discharging_sio2,
    discharging_moisture,
    discharging_cr,
    discharging_co,
    final_wmt,
    final_moisture,
    final_ni,
    final_fe,
    base_price,
    final_price,
    boulders_tonnage,
    boulders_processing_cost,
    boulders_freight_cost,
    dead_freight,
    despatch,
    lab_name,
    buyer_name,
    avg(distance_from_wharf) distance_from_wharf
FROM cte
GROUP BY
    year,
    month,
    shipment,
    arrival,
    loading_start,
    loading_end,
    vessel,
    target_wmt,
    target_moisture,
    spec_ni,
    spec_fe,
    destination,
    loading_wmt,
    loading_dmt,
    loading_ni,
    loading_fe,
    loading_mgo,
    loading_sio2,
    loading_moisture,
    loading_cr,
    loading_co,
    discharging_wmt,
    discharging_dmt,
    discharging_ni,
    discharging_fe,
    discharging_mgo,
    discharging_sio2,
    discharging_moisture,
    discharging_cr,
    discharging_co,
    final_wmt,
    final_moisture,
    final_ni,
    final_fe,
    base_price,
    final_price,
    boulders_tonnage,
    boulders_processing_cost,
    boulders_freight_cost,
    dead_freight,
    despatch,
    lab_name,
    buyer_name
ORDER BY
    loading_end,
    shipment,
    arrival
