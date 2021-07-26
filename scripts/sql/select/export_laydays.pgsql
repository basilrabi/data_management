SELECT
    EXTRACT(year FROM ld_statement.completed_loading)::integer AS year,
    EXTRACT(month FROM ld_statement.completed_loading)::integer AS month,
    shipment.name,
    detail_from.laytime_rate,
	REPLACE(detail_from.interval_from::text, '+08', '') as interval_start,
    REPLACE(detail_to.interval_from::text, '+08', '') as interval_end,
    EXTRACT(
        epoch FROM detail_to.interval_from - detail_from.interval_from
    ) * detail_from.laytime_rate / (100 * 60 * 60 * 24) lay_days,
    detail_from.interval_class,
    detail_from.remarks
FROM shipment_laydaysdetailcomputed detail_from
    LEFT JOIN LATERAL (
        SELECT *
        FROM shipment_laydaysdetailcomputed a
        WHERE a.laydays_id = detail_from.laydays_id
            AND a.interval_from > detail_from.interval_from
        ORDER BY a.interval_from ASC
        LIMIT 1
    ) detail_to ON true
    LEFT JOIN shipment_laydaysstatement ld_statement
        ON ld_statement.id = detail_from.laydays_id
    LEFT JOIN shipment_shipment shipment
        ON shipment.id = ld_statement.id
WHERE detail_to.interval_from IS NOT NULL
    AND ld_statement.completed_loading IS NOT NULL
ORDER BY
    ld_statement.completed_loading,
    shipment.name,
    detail_from.interval_from
