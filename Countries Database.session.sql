-- Check before update
SELECT COUNT(*)
FROM wdi_country
WHERE `Short Name` = 'Venezuela';

-- Perform update
UPDATE wdi_country
SET Region = 'Latin America & Caribbean', `Income Group` = 'High income'
WHERE `Short Name` = 'Venezuela';

-- Check after update
SELECT COUNT(*)
FROM wdi_country
WHERE `Short Name` = 'Venezuela';
