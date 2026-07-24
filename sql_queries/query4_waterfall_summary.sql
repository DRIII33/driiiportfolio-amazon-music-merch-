-- Purpose: Pre-aggregate and format financial ledger entries vertically.
--          Prepares clean absolute data structures for the native Looker Studio Waterfall Widget.

CREATE OR REPLACE VIEW `driiiportfolio.amazon_music_merch.waterfall_summary_view` AS
SELECT
  '1. Gross Revenue' AS metric_category,
  ROUND(SUM(gross_revenue), 2) AS metric_value
FROM `driiiportfolio.amazon_music_merch.reconciled_aggregation_view`

UNION ALL

SELECT
  '2. COGS Deductions' AS metric_category,
  ROUND(SUM(total_cogs), 2) AS metric_value -- FIXED: Kept positive for Looker Studio's engine
FROM `driiiportfolio.amazon_music_merch.reconciled_aggregation_view`

UNION ALL

SELECT
  '3. Shipping Fees' AS metric_category,
  ROUND(SUM(total_shipping), 2) AS metric_value -- FIXED: Kept positive for Looker Studio's engine
FROM `driiiportfolio.amazon_music_merch.reconciled_aggregation_view`

UNION ALL

SELECT
  '4. Guaranteed Minimum Burdens' AS metric_category,
  ROUND(SUM(upfront_commitment), 2) AS metric_value -- FIXED: Kept positive for Looker Studio's engine
FROM `driiiportfolio.amazon_music_merch.deal_valuation_view` -- Standardized to your view name

UNION ALL

SELECT
  '5. Net Amazon Operating Position' AS metric_category,
  ROUND(SUM(net_amazon_profit_contribution), 2) AS metric_value
FROM `driiiportfolio.amazon_music_merch.deal_valuation_view`; -- Standardized to your view name
