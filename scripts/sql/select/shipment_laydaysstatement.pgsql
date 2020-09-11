SELECT
    a.arrival_pilot,
    a.arrival_tmc,
    a.can_test,
    a.can_test_factor,
    a.cargo_description,
    a.date_saved,
    a.demurrage_rate,
    a.despatch_rate,
    a.laytime_terms,
    a.loading_terms,
    a.negotiated,
    a.nor_accepted,
    a.nor_tender,
    a.pre_loading_can_test,
    a.remarks,
    a.report_date,
    a.revised,
    a.tonnage,
    a.vessel_voyage,
    b.name
FROM shipment_laydaysstatement a
    LEFT JOIN shipment_shipment b
        ON a.shipment_id = b.id
ORDER BY a.completed_loading, b.name
