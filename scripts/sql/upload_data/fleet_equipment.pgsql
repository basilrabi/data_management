CREATE TEMPORARY TABLE temp_fleet_equipment
(
    fleet_number smallint,
    acquisition_cost numeric(12,2),
    date_acquired date,
    date_phased_out date,
    serial_number character varying(100),
    model_name character varying(20),
    owner_name character varying(20)
);

\copy temp_fleet_equipment FROM 'data/fleet_equipment.csv' DELIMITER ',' CSV;

INSERT INTO fleet_equipment (
    fleet_number,
    acquisition_cost,
    date_acquired,
    date_phased_out,
    serial_number,
    model_id,
    owner_id
)
SELECT
    a.fleet_number,
    a.acquisition_cost,
    a.date_acquired,
    a.date_phased_out,
    a.serial_number,
    b.id,
    c.id
FROM temp_fleet_equipment a
    LEFT JOIN fleet_equipmentmodel b
        ON a.model_name = b.name
    LEFT JOIN organization_organization c
        ON a.owner_name = c.name;
