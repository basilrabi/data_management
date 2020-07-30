CREATE TEMPORARY TABLE temp_shipment_laydaysstatement
(
    arrival_pilot timestamp with time zone,
    arrival_tmc timestamp with time zone,
    can_test smallint,
    can_test_factor numeric(2,1),
    cargo_description character varying(20),
    date_saved timestamp with time zone,
    demurrage_rate smallint,
    despatch_rate smallint,
    loading_terms smallint,
    nor_accepted timestamp with time zone,
    nor_tender timestamp with time zone,
    pre_loading_can_test boolean,
    report_date date,
    revised boolean,
    tonnage integer,
    vessel_voyage smallint,
    shipment_name character varying(10)
);

\copy temp_shipment_laydaysstatement FROM 'data/shipment_laydaysstatement.csv' DELIMITER ',' CSV;

INSERT INTO shipment_laydaysstatement (
    additional_laytime,
    arrival_pilot,
    arrival_tmc,
    can_test,
    can_test_factor,
    cargo_description,
    date_saved,
    demurrage,
    demurrage_rate,
    despatch,
    despatch_rate,
    loading_terms,
    nor_accepted,
    nor_tender,
    pre_loading_can_test,
    report_date,
    revised,
    time_allowed,
    tonnage,
    vessel_voyage,
    shipment_id
)
SELECT
    '00:00:00',
    a.arrival_pilot,
    a.arrival_tmc,
    a.can_test,
    a.can_test_factor,
    a.cargo_description,
    a.date_saved,
    0,
    a.demurrage_rate,
    0,
    a.despatch_rate,
    a.loading_terms,
    a.nor_accepted,
    a.nor_tender,
    a.pre_loading_can_test,
    a.report_date,
    a.revised,
    '00:00:00',
    a.tonnage,
    a.vessel_voyage,
    b.id
FROM temp_shipment_laydaysstatement a
    LEFT JOIN shipment_shipment b
        ON b.name = a.shipment_name
