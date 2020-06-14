SELECT
	shipment_trip.id lct_trip,
	shipment_lct.name lct,
	shipment_vessel.name vessel,
	replace(tab1.interval_from::text, '+08', '') as from,
	tab2.to,
	tab1.interval_class,
	tab1.remarks as remarks
FROM shipment_tripdetail tab1
	LEFT JOIN shipment_trip
		ON tab1.trip_id = shipment_trip.id
	LEFT JOIN shipment_lct
		ON shipment_trip.lct_id = shipment_lct.id
	LEFT JOIN shipment_vessel
		ON shipment_trip.vessel_id = shipment_vessel.id
	LEFT JOIN LATERAL (
		SELECT replace(shipment_tripdetail.interval_from::text, '+08', '') as to
		FROM shipment_tripdetail
		WHERE shipment_tripdetail.interval_from > tab1.interval_from
			AND shipment_tripdetail.trip_id = tab1.trip_id
		LIMIT 1
	) tab2 ON true
WHERE tab2.to IS NOT NULL
ORDER BY
	shipment_trip.id,
	tab1.interval_from
