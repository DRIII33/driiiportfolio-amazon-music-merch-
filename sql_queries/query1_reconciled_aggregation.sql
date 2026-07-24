-- Purpose: Join transactional sales records with contract variables.
--          Computes Gross Margin performance and cumulative accrued royalties
--          by month, category, and artist tier to prevent overpayment leakage.
CREATE OR REPLACE VIEW `driiiportfolio.amazon_music_merch.reconciled_aggregation_view` AS
SELECT
  LAST_DAY(EXTRACT(DATE FROM s.timestamp), MONTH) AS accounting_month,
  c.artist_tier,
  s.product_category,
  SUM(s.units_sold) AS total_units,
  ROUND(SUM(s.units_sold * s.unit_retail_price), 2) AS gross_revenue,
  ROUND(SUM(s.units_sold * s.unit_manufacturing_cost), 2) AS total_cogs,
  ROUND(SUM(s.units_sold * s.shipping_fees), 2) AS total_shipping,
  -- Calculate Net Revenue post physical handling costs
  ROUND(SUM(s.units_sold * s.unit_retail_price) - SUM(s.units_sold * s.unit_manufacturing_cost) - SUM(s.units_sold * s.shipping_fees), 2) AS net_revenue,
  -- Calculate Gross Margin %
  ROUND(SAFE_DIVIDE(SUM(s.units_sold * s.unit_retail_price) - SUM(s.units_sold * s.unit_manufacturing_cost), SUM(s.units_sold * s.unit_retail_price)), 4) AS gross_margin_percentage,
  -- Calculate accrued variable royalty liabilities before contract recoupment checks
  ROUND(SUM((s.units_sold * s.unit_retail_price) - (s.units_sold * s.unit_manufacturing_cost) - (s.units_sold * s.shipping_fees)) * ANY_VALUE(c.revenue_share_split), 2) AS accrued_earned_royalties
FROM
  `driiiportfolio.amazon_music_merch.fact_merch_sales` AS s
INNER JOIN
  `driiiportfolio.amazon_music_merch.dim_artist_contracts` AS c
ON
  s.artist_id = c.artist_id
GROUP BY
  accounting_month,
  c.artist_tier,
  s.product_category
ORDER BY
  accounting_month DESC,
  gross_revenue DESC;
