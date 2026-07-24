-- Purpose: Isolate hidden operational bottlenecks across physical facilities.
--          Tracks total units scrapped/damaged, net inventory turnover velocity,
--          and true holding cost burdens to flag unbudgeted capital drift.
CREATE OR REPLACE VIEW `driiiportfolio.amazon_music_merch.supply_chain_optimization_view` AS
WITH warehouse_summaries AS (
  SELECT
    warehouse_id,
    artist_id,
    SUM(units_received) AS total_received,
    SUM(units_damaged) AS total_damaged,
    ROUND(SUM(units_received * days_in_storage * daily_unit_holding_cost), 2) AS cumulative_carrying_cost,
    ROUND(AVG(days_in_storage), 1) AS average_days_held
  FROM
    `driiiportfolio.amazon_music_merch.fact_inventory_logs`
  GROUP BY
    warehouse_id,
    artist_id
),
sales_velocity AS (
  SELECT
    artist_id,
    SUM(units_sold) AS total_units_sold
  FROM
    `driiiportfolio.amazon_music_merch.fact_merch_sales`
  GROUP BY
    artist_id
)
SELECT
  w.warehouse_id,
  c.artist_name,
  c.artist_id, -- Include artist_id for potential joins/breakdowns
  w.total_received,
  w.total_damaged,
  -- Calculate stock damage leakage percentage
  ROUND(SAFE_DIVIDE(w.total_damaged, w.total_received), 4) AS scrap_rate_percentage,
  w.cumulative_carrying_cost,
  w.average_days_held,
  -- Dynamic Inventory Turnover Ratio (Annualized proxy based on total sales)
  ROUND(SAFE_DIVIDE(COALESCE(v.total_units_sold, 0), SAFE_DIVIDE(w.total_received, 12)), 2) AS inventory_turnover_velocity
FROM
  warehouse_summaries AS w
INNER JOIN
  `driiiportfolio.amazon_music_merch.dim_artist_contracts` AS c ON w.artist_id = c.artist_id
LEFT JOIN
  sales_velocity AS v ON w.artist_id = v.artist_id;
-- WHERE clause from original query not included in view for flexibility in Looker Studio filtering
