WITH cte_a AS (
    SELECT
        a.images_in_pdf,
        a.mgb_receipt,
        a.video,
        b.name shipment,
        c.arrival_tmc,
        MAX(d.interval_from) laytime_end
    FROM shipment_draftsurvey a
        LEFT JOIN shipment_shipment b
            ON a.shipment_id = b.id
        LEFT JOIN shipment_laydaysstatement c
            ON b.id = c.shipment_id
        LEFT JOIN shipment_laydaysdetail d
            ON c.id = d.laydays_id
    GROUP BY
        a.images_in_pdf,
        a.mgb_receipt,
        a.video,
        b.name,
        c.arrival_tmc
)
SELECT
    images_in_pdf,
    mgb_receipt,
    shipment,
    video
FROM cte_a
ORDER BY
    laytime_end DESC,
    arrival_tmc DESC,
    shipment DESC

