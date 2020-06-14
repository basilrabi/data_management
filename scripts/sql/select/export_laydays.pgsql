SELECT
	shipment_shipment.name,
	replace(tab1.interval_from::text, '+08', '') as from,
	tab2.to,
	tab1.interval_class,
	tab1.remarks as remarks_from,
	tab2.remarks as remarks_to
FROM shipment_laydaysdetail tab1
	LEFT JOIN shipment_laydaysstatement
		ON tab1.laydays_id = shipment_laydaysstatement.id
	LEFT JOIN shipment_shipment
		ON shipment_laydaysstatement.shipment_id = shipment_shipment.id
	LEFT JOIN LATERAL (
		SELECT
			replace(shipment_laydaysdetail.interval_from::text, '+08', '') as to,
			shipment_laydaysdetail.remarks
		FROM shipment_laydaysdetail
		WHERE shipment_laydaysdetail.interval_from > tab1.interval_from
			AND shipment_laydaysdetail.laydays_id = tab1.laydays_id
		LIMIT 1
	) tab2 ON true
WHERE tab2.to IS NOT NULL
