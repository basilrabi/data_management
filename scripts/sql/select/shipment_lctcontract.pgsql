SELECT b.name, a.start, a.end
FROM shipment_lctcontract a
    LEFT JOIN shipment_lct b
        ON a.lct_id = b.id
ORDER BY b.name, a.start
