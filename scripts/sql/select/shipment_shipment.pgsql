WITH cte_a AS (
    SELECT
        a.base_price,
        a.boulders_freight_cost,
        a.boulders_processing_cost,
        a.boulders_tonnage,
        a.demurrage,
        a.despatch,
        a.dump_truck_trips,
        a.final_fe,
        a.final_moisture,
        a.final_ni,
        a.final_price,
        a.name,
        a.remarks,
        a.spec_fe,
        a.spec_moisture,
        a.spec_ni,
        a.spec_tonnage,
        a.target_tonnage,
        b.name buyer,
        d.name destination,
        p.name product,
        v.name vessel,
        l.arrival_tmc,
        MAX(ld.interval_from) laytime_end
    FROM shipment_shipment a
        LEFT JOIN shipment_buyer b
            ON b.id = a.buyer_id
        LEFT JOIN shipment_destination d
            ON d.id = a.destination_id
        LEFT JOIN shipment_laydaysstatement l
            ON l.shipment_id = a.id
        LEFT JOIN shipment_laydaysdetail ld
            ON ld.laydays_id = l.id
        LEFT JOIN shipment_product p
            ON p.id = a.product_id
        LEFT JOIN shipment_vessel v
            ON v.id = a.vessel_id
    GROUP BY
        a.base_price,
        a.boulders_freight_cost,
        a.boulders_processing_cost,
        a.boulders_tonnage,
        a.demurrage,
        a.despatch,
        a.dump_truck_trips,
        a.final_fe,
        a.final_moisture,
        a.final_ni,
        a.final_price,
        a.name,
        a.remarks,
        a.spec_fe,
        a.spec_moisture,
        a.spec_ni,
        a.spec_tonnage,
        a.target_tonnage,
        b.name,
        d.name,
        p.name,
        v.name,
        l.arrival_tmc
)
SELECT
    base_price,
    boulders_freight_cost,
    boulders_processing_cost,
    boulders_tonnage,
    demurrage,
    despatch,
    dump_truck_trips,
    final_fe,
    final_moisture,
    final_ni,
    final_price,
    name,
    remarks,
    spec_fe,
    spec_moisture,
    spec_ni,
    spec_tonnage,
    target_tonnage,
    buyer,
    destination,
    product,
    vessel
FROM cte_a
ORDER BY
    laytime_end DESC,
    arrival_tmc DESC,
    name DESC
