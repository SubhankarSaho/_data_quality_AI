SELECT
    DATE(claim_date) AS date,
    ROUND(
        SUM(
            CASE
                WHEN claim_status = 'APPROVED' THEN 1
                ELSE 0
            END
        ) * 100.0 / CAST(COUNT(*) AS FLOAT),
        2
    ) AS value
FROM insurance_claims
GROUP BY DATE(claim_date)
ORDER BY DATE(claim_date);
