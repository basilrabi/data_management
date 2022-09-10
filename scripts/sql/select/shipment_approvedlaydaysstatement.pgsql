SELECT
    s.name,
    a.approved,
    a.signed_statement
FROM shipment_approvedlaydaysstatement a
    LEFT JOIN shipment_laydaysstatement b
        ON b.id = a.statement_id
    LEFT JOIN shipment_shipment s
        ON s.id = b.shipment_id
WHERE a.approved or a.signed_statement IS NOT NULL
ORDER BY b.completed_loading DESC
