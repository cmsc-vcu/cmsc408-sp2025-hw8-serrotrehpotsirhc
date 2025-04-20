# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
from helpers import create_database_engine, run_sql_and_return_df, run_sql_and_return_html, create_db_wrapper, execute_ddl_from_file, execute_ddl

# Load these variables from .env file.
config_map = {
  'user': "CMSC408_HW8_USER",
  'password': "CMSC408_HW8_PASSWORD",
  'host': "CMSC408_HW8_HOST",
  'database': "CMSC408_HW8_DB_NAME"
}

cnx,config = create_db_wrapper( config_map )
  
#
#
#
#
# Do a quick test of the connection and trap the errors better!

run_sql_and_return_html(cnx,"""
select
  table_schema, table_name, table_rows
from
  information_schema.tables
where
  table_schema in ('world_bank_data')
""")

#
#
#
#
#
#
#
#
#
#
#
# How many records are in the world_bank_data.wdi_country table?
# (skills: select, aggregate)

run_sql_and_return_html(cnx,"""
select
  count(*) as "Row Count"
from
  world_bank_data.wdi_country
""")

#
#
#
#
#
#
#
## write out the first 10 records and look at the columns
## Do you see any blanks or missing data?
## (skills: select, limit)

run_sql_and_return_html(cnx,"""
select
  *
from 
  world_bank_data.wdi_country
limit 5
""")

#
#
#
#
#
#
#
#
## task 3
## Which records are NOT for countries, that is they're for regions or groups of countries.
## How can you tell?
## Once you figure it out, write a query to list all the non-countries
## (skills: select, where)

run_sql_and_return_html(cnx,"""
SELECT `Short Name`
FROM world_bank_data.wdi_country
WHERE `Region` IS NULL
ORDER BY `Short Name`;
""")
#
#
#
#
#
#
#
## task 4
## The WDI table clearly contains information for countries and non-countries
## using CREATE TABLE ... SELECT from WHERE syntax.
## Finally, below write a query to return the number
## of records in the new table.
## (skills: select, aggregate)

# drop table
execute_ddl(cnx,"""
drop table if exists wdi_country;
""")
#
#
#
#
# create table
execute_ddl(cnx,"""
CREATE TABLE wdi_country AS
SELECT *
FROM world_bank_data.wdi_country
WHERE Region IS NOT NULL;
""")
#
#
#
# show number of records
run_sql_and_return_html(cnx,"""
SELECT
  COUNT(*) AS "Row Count"
FROM
  wdi_country
""")
#
#
#
#
#
#
#
## (skills: select, aggregate)

run_sql_and_return_html(cnx,"""
SELECT COUNT(*) AS "Country Count"
FROM world_bank_data.wdi_country
WHERE Region IS NOT NULL;
""")

#
#
#
#
#
#
#
## Let's investigate the country_region field.
## What is the domain of the country_region field? That is,
## what are the unique values found there?
## (there are several possible ways to code this in SQL)
## (skills: select, aggregate, order by)

run_sql_and_return_html(cnx,"""
SELECT DISTINCT Region
FROM world_bank_data.wdi_country
WHERE Region IS NOT NULL
ORDER BY Region;
""")

#
#
#
#
#
#
#
## How many countries are in each region?
## (skills: select, aggregate, group by, order by)

run_sql_and_return_html(cnx,"""
SELECT
  Region,
  COUNT(*) AS "Country Count"
FROM
  world_bank_data.wdi_country
WHERE
  `Income Group` IS NOT NULL
GROUP BY
  Region
ORDER BY
  Region
""")

#
#
#
#
#
#
#
## List the country full names and regions for all countries in north america
## (skills: select, where, order by)

run_sql_and_return_html(cnx,"""
SELECT
  `Long Name`,
  Region
FROM
  world_bank_data.wdi_country
WHERE
  Region = 'North America'
  AND `Income Group` IS NOT NULL
ORDER BY
  `Long Name`
""")

#
#
#
#
#
## The last World Cup soccer tournament was hosted by Qatar.
## What region contains Qatar?  List the region, country short name and full name
## (skills: select, where)

run_sql_and_return_html(cnx,"""
SELECT
  Region,
  `Short Name`,
  `Long Name`
FROM
  world_bank_data.wdi_country
WHERE
  `Short Name` = 'Qatar'
  OR `Long Name` = 'Qatar'
""")

#
#
#
#
#
## There are two abbreviation fields in the data country_abbr and country_wb_abbr.
## List the country code, short name, abbr, wb_abbr and region for all the countries
## where the abbr and wb_abbr are different.
## (skills: select, where, order by)

run_sql_and_return_html(cnx,"""
SELECT
  `Country Code`,
  `Short Name`,
  `2-alpha code`,
  `WB-2 code`,
  Region
FROM
  world_bank_data.wdi_country
WHERE
  `2-alpha code` != `WB-2 code`
  AND `Income Group` IS NOT NULL
ORDER BY
  `Short Name`
""")

#
#
#
#
#
## Now, let's investigate the "income category" field.
## List the income categories and the number of countries in each
## income category in descending order of most countries to least.
## (skills: select, aggregate, group by, order by)

run_sql_and_return_html(cnx,"""
SELECT
  `Income Group` AS "Income Category",
  COUNT(*) AS "Country Count"
FROM
  world_bank_data.wdi_country
GROUP BY
  `Income Group`
ORDER BY
  "Country Count" DESC;
""")

#
#
#
#
#
## This task depends on fixing Task 11. 1 country has NULL for income but has a region: Brunei Darussalam. All others are aggregates (non-countries).

run_sql_and_return_html(cnx,"""
SELECT
  `Short Name`,
  `Region`,
  `Income Group`
FROM
  world_bank_data.wdi_country
WHERE
  `Income Group` IS NULL
  AND Region IS NOT NULL;
""")

#
#
#
#
#
## OK, this HAS to be an error. Let's make a assumption that the country 
## in question, because they are oil-rich, are "high income".  
## Write an update comment to correct the issue.
## NOTE - if you get this wrong, all subsequent tables will be wrong!

execute_ddl(cnx,"""
UPDATE wdi_country
SET 
  Region = 'Latin America & Caribbean',
  `Income Group` = 'High income'
WHERE 
  `Short Name` = 'Venezuela';
COMMIT;  
""")
```
#
## Now, display the country again to verify the change stuck!

run_sql_and_return_html(cnx,"""
SELECT
  `Short Name`,
  `Table Name`,
  `Income Group`
FROM
  wdi_country
WHERE
  `Short Name` LIKE 'Venezuela';
""")

#
#
#
#
#
## Write a single query that show the number of countries in each 
## "Region"-"Income Group" pair.  The table should have 3 columns:
## region, income group, and no.of.countries.
## (skills: select, aggregate, group by, order by)

run_sql_and_return_html(cnx,"""
SELECT
  Region,
  `Income Group`,
  COUNT(*) AS "no.of.countries"
FROM
  world_bank_data.wdi_country
WHERE
  `Income Group` IS NOT NULL
GROUP BY
  Region,
  `Income Group`
ORDER BY
  Region,
  `Income Group`
""")

#
#
#
#
#
## Examine the result from task 14. It would be really cool to
## present the results of this table in a 2-D form, with 
## columns for each income category (high, upper middle, lower middle, low, other)
## regions down the side, and the pair-wise count inside each cell.
## Using CASE statements, DO IT!  BE SURE to include the countries without
## an income category.

## HINT - your query should return 6 columns: the region name, one
## column for each of the income categories (e.g., High, Upper middle, etc.)
## and a column for the row totals.
## (skills: select, aggregate, group by, nested query)

run_sql_and_return_html(cnx,"""
SELECT
  COALESCE(`Region`, 'Other') AS region,
  SUM(CASE WHEN `Income Group` = 'High income' THEN 1 ELSE 0 END) AS high_income,
  SUM(CASE WHEN `Income Group` = 'Upper middle income' THEN 1 ELSE 0 END) AS upper_middle_income,
  SUM(CASE WHEN `Income Group` = 'Lower middle income' THEN 1 ELSE 0 END) AS lower_middle_income,
  SUM(CASE WHEN `Income Group` = 'Low income' THEN 1 ELSE 0 END) AS low_income,
  SUM(CASE WHEN `Income Group` IS NULL THEN 1 ELSE 0 END) AS other_income,
  CAST(COUNT(*) AS DECIMAL(5,1)) AS row_total
FROM wdi_country
GROUP BY COALESCE(`Region`, 'Other')
ORDER BY region;

""")

#
#
#
#
#
## Wow! what a cool table!  It is very interesting to see where the money
## sits around the world.  Using the general approach from Task 14 above
## and write a query to return the single region with the most lower-income
## countries.

## Your query should return 3 columns, the number of 
## low-income countries, the region name and the income group

## PUT THE NUMBER FIRST! (use: count, region name, income group)
## (skills: select, aggregate, group by, nested query, order by, limit)

run_sql_and_return_html(cnx,"""
SELECT
  COUNT(*) AS "Low Income Count",
  Region,
  'Low income' AS "Income Group"
FROM
  wdi_country
WHERE
  `Income Group` = 'Low income'
GROUP BY
  Region
ORDER BY
  COUNT(*) DESC
LIMIT 1;
""")

#
#
#
#
#
## Are you getting the hand of this? Good! We need to take a look at all
## the countries in the same region and with the same income category as
## the Marshall Islands.
## For each country that matches, print their country code, short name,
## region and income category, by order of their short name.  As a hint,
## the country code for the Marshall Islands is MHL.
## (skills: select, where, subquery)

run_sql_and_return_html(cnx,"""
SELECT
  `Country Code`,
  `Short Name`,
  Region,
  `Income Group`
FROM
  world_bank_data.wdi_country
WHERE
  Region = (
    SELECT Region
    FROM world_bank_data.wdi_country
    WHERE `Country Code` = 'MHL'
  )
  AND `Income Group` = (
    SELECT `Income Group`
    FROM world_bank_data.wdi_country
    WHERE `Country Code` = 'MHL'
  )
  AND `Income Group` IS NOT NULL
ORDER BY
  `Short Name`
""")

#
#
#
#
#
## OK - let's raise the heat in the kitchen! Review the output from task 14.
## You'll see that some of the regions do not contain all of the income
## levels.  For example, the Europe & Central Asia region does not have
## any low income countries.
##
## CHALLENGE - using a SINGLE SQL statement, write a table that contains every
## combination of region and income category (including the missing '') values!
##
## THEN add a WHERE clause to only show the values that were missing from
## the original pairings!
##
## HINT - there should be AT MOST [# of regions]x[# of income cats] = 28
## rows in your final table, and there are 22 rows returned in the query
## in Task 14.  (FYI - I get 6 rows in my final table.)
## (skills: select, where, subqueries, joins)

run_sql_and_return_html(cnx,"""
WITH AllPairs AS (
  SELECT
    r.Region,
    i.`Income Group`
  FROM
    (SELECT DISTINCT Region FROM world_bank_data.wdi_country WHERE Region IS NOT NULL) r
    CROSS JOIN
    (SELECT DISTINCT `Income Group` FROM world_bank_data.wdi_country WHERE `Income Group` IS NOT NULL) i
),
ExistingPairs AS (
  SELECT DISTINCT
    Region,
    `Income Group`
  FROM
    world_bank_data.wdi_country
  WHERE
    `Income Group` IS NOT NULL
)
SELECT
  ap.Region,
  ap.`Income Group`,
  'Missing' AS Status
FROM AllPairs ap
LEFT JOIN ExistingPairs ep
  ON ap.Region = ep.Region AND ap.`Income Group` = ep.`Income Group`
WHERE ep.Region IS NULL
ORDER BY ap.Region, ap.`Income Group`;
""")

#
#
#
#
#
## Hot enough, yet?  Let's go for ghost-pepper HOT!  Now let's build some
## percentage tables.  For example, across the entire sample, what
## is the percentage of total countries in each income category?
##
## As a first step, build off the result from task 14 and create a table with
## six columns (region, income cat, country count, sum of countries in region,
## sum of countries by income and total sum countries).
##
## THEN, add a 7th column calculating the percent of total for each,
## region-income pair.
##
## actually calculating percentages and print out a table will be a
## slam dunk after this!
## (skills: select, where, subqueries, joins, aggregate functions)

run_sql_and_return_html(cnx,"""
WITH base AS (
  SELECT
    COALESCE(`Region`, 'Other') AS region,
    `Income Group` AS income_group,
    COUNT(*) AS count
  FROM wdi_country
  GROUP BY COALESCE(`Region`, 'Other'), `Income Group`
),
totals AS (
  SELECT
    region,
    SUM(count) AS region_total
  FROM base
  GROUP BY region
),
overall_total AS (
  SELECT SUM(count) AS grand_total FROM base
),
income_totals AS (
  SELECT income_group, SUM(count) AS income_total
  FROM base
  GROUP BY income_group
)
SELECT
  b.region,
  b.income_group,
  b.count,
  t.region_total,
  i.income_total,
  o.grand_total,
  ROUND(100.0 * b.count / o.grand_total, 2) AS pct_of_total
FROM base b
JOIN totals t ON b.region = t.region
JOIN income_totals i ON b.income_group = i.income_group
CROSS JOIN overall_total o
ORDER BY b.region, b.income_group;
""")


#
#
#
#
#
## SLAM DUNK TIME!  Using the resulting table CTEs from Task 19,
## print table similar to the table in Task 15, with Income group in the
## columns, Region in the rows and Percent of total in each cell of the table.

run_sql_and_return_html(cnx,"""
WITH Counts AS (
  SELECT
    Region,
    `Income Group`,
    COUNT(*) AS country_count
  FROM
    world_bank_data.wdi_country
  WHERE
    Region IS NOT NULL AND `Income Group` IS NOT NULL
  GROUP BY
    Region, `Income Group`
),
GrandTotal AS (
  SELECT
    SUM(country_count) AS total_countries
  FROM
    Counts
)
SELECT
  c.Region,
  ROUND(SUM(CASE WHEN c.`Income Group` = 'High income' THEN (c.country_count / g.total_countries) * 100 ELSE 0 END), 2) AS "High",
  ROUND(SUM(CASE WHEN c.`Income Group` = 'Upper middle income' THEN (c.country_count / g.total_countries) * 100 ELSE 0 END), 2) AS "Upper middle",
  ROUND(SUM(CASE WHEN c.`Income Group` = 'Lower middle income' THEN (c.country_count / g.total_countries) * 100 ELSE 0 END), 2) AS "Lower middle",
  ROUND(SUM(CASE WHEN c.`Income Group` = 'Low income' THEN (c.country_count / g.total_countries) * 100 ELSE 0 END), 2) AS "Low",
  ROUND(SUM(c.country_count / g.total_countries) * 100, 2) AS "Total"
FROM
  Counts c
CROSS JOIN
  GrandTotal g
GROUP BY
  c.Region
ORDER BY
  c.Region;
""")

#
#
#
#
#
## ANOTHER DUNK!  Using the resulting table CTEs from Task 19,
## print a table listing the number, totals and percentage of countries
## by income category.

## (This is much simpler than task 20!)

run_sql_and_return_html(cnx,"""
WITH Counts AS (
  SELECT
    `Income Group`,
    COUNT(*) AS country_count
  FROM
    wdi_country
  WHERE
    `Income Group` IS NOT NULL
  GROUP BY
    `Income Group`
),
GrandTotal AS (
  SELECT
    COUNT(*) AS total_countries
  FROM
    wdi_country
  WHERE
    `Income Group` IS NOT NULL
)
SELECT
  c.`Income Group`,
  c.country_count,
  g.total_countries,
  ROUND((c.country_count * 100.0 / g.total_countries), 1) AS "Percent of Total"
FROM
  Counts c
CROSS JOIN
  GrandTotal g
ORDER BY
  c.country_count DESC;
""")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
