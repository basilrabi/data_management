CREATE TEMPORARY TABLE temp_shipment_shipment
(
    base_price numeric(5,2),
    boulders_freight_cost numeric(8,2),
    boulders_processing_cost numeric(8,2),
    boulders_tonnage integer,
    dead_freight numeric(8,2),
    demurrage numeric(8,2),
    despatch numeric(8,2),
    dump_truck_trips smallint,
    final_fe numeric(6,4),
    final_moisture numeric(6,4),
    final_ni numeric(6,4),
    final_price numeric(5,2),
    name character varying(10),
    remarks text,
    spec_fe numeric(4,2),
    spec_moisture numeric(4,2),
    spec_ni numeric(4,2),
    spec_tonnage integer,
    target_tonnage integer,
    buyer_name character varying(40),
    destination_name character varying(40),
    product_name character varying(40),
    vessel_name character varying(50)
);

\copy temp_shipment_shipment FROM 'data/shipment_shipment.csv' DELIMITER ',' CSV;

INSERT INTO shipment_shipment (
    base_price,
    boulders_freight_cost,
    boulders_processing_cost,
    boulders_tonnage,
    buyer_id,
    dead_freight,
    demurrage,
    despatch,
    destination_id,
    dump_truck_trips,
    final_fe,
    final_moisture,
    final_ni,
    final_price,
    name,
    product_id,
    remarks,
    spec_fe,
    spec_moisture,
    spec_ni,
    spec_tonnage,
    target_tonnage,
    vessel_id
)
SELECT
    a.base_price,
    a.boulders_freight_cost,
    a.boulders_processing_cost,
    a.boulders_tonnage,
    b.id,
    a.dead_freight,
    a.demurrage,
    a.despatch,
    d.id,
    a.dump_truck_trips,
    a.final_fe,
    a.final_moisture,
    a.final_ni,
    a.final_price,
    a.name,
    p.id,
    a.remarks,
    a.spec_fe,
    a.spec_moisture,
    a.spec_ni,
    a.spec_tonnage,
    a.target_tonnage,
    v.id
FROM temp_shipment_shipment a
    LEFT JOIN shipment_buyer b
        ON b.name = a.buyer_name
    LEFT JOIN shipment_destination d
        ON d.name = a.destination_name
    LEFT JOIN shipment_product p
        ON p.name = a.product_name
    LEFT JOIN shipment_vessel v
        ON v.name = a.vessel_name
