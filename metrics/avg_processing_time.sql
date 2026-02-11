SELECT
    DATE(claim_date) AS date,
    ROUND(AVG(processing_days), 2) AS value
FROM insurance_claims
GROUP BY DATE(claim_date)
ORDER BY DATE(claim_date);
