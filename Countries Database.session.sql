SELECT
  Region,
  SUM(CASE WHEN `Income Group` = 'High income' THEN 1 ELSE 0 END) AS "High",
  SUM(CASE WHEN `Income Group` = 'Upper middle income' THEN 1 ELSE 0 END) AS "Upper middle",
  SUM(CASE WHEN `Income Group` = 'Lower middle income' THEN 1 ELSE 0 END) AS "Lower middle",
  SUM(CASE WHEN `Income Group` = 'Low income' THEN 1 ELSE 0 END) AS "Low",
  SUM(CASE WHEN `Income Group` IS NULL THEN 1 ELSE 0 END) AS "Other"
FROM
  world_bank_data.wdi_country
WHERE
  Region IS NOT NULL
GROUP BY
  Region
ORDER BY
  Region;