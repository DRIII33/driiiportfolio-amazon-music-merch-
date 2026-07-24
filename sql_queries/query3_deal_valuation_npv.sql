-- Purpose: Enterprise portfolio grading ledger. Evaluates every active asset contract
--          to calculate real-time net returns, actual profit yields, and identify unrecouped
--          sunk risks where deployed capital fails to hit performance expectations.
CREATE OR REPLACE VIEW `driiiportfolio.amazon_music_merch.deal_valuation_view` AS
WITH compiled_sales AS (
  SELECT
    artist_id,
    ROUND(SUM(net_revenue), 2) AS life_to_date_net_revenue
  FROM
    `driiiportfolio.amazon_music_merch.fact_merch_sales`
  GROUP BY
    artist_id
)
SELECT
  c.artist_id,
  c.artist_name,
  c.artist_tier,
  c.guaranteed_minimum_royalty AS upfront_commitment,
  COALESCE(s.life_to_date_net_revenue, 0.00) AS net_revenue_yield,
  -- Calculate accrued artist split earnings
  ROUND(COALESCE(s.life_to_date_net_revenue, 0.00) * c.revenue_share_split, 2) AS artist_earned_royalties,
  -- Recoupment flag logic validation
  CASE
    WHEN (COALESCE(s.life_to_date_net_revenue, 0.00) * c.revenue_share_split) >= c.guaranteed_minimum_royalty THEN TRUE
    ELSE FALSE
  END AS recoupment_milestone_achieved,
  -- Unrecouped balance calculation (Sunk cost risk exposure)
  CASE
    WHEN (COALESCE(s.life_to_date_net_revenue, 0.00) * c.revenue_share_split) >= c.guaranteed_minimum_royalty THEN 0.00
    ELSE ROUND(c.guaranteed_minimum_royalty - (COALESCE(s.life_to_date_net_revenue, 0.00) * c.revenue_share_split), 2)
  END AS unrecouped_sunk_balance,
  -- Amazon Net Position profit contribution
  ROUND(COALESCE(s.life_to_date_net_revenue, 0.00) - CASE
    WHEN (COALESCE(s.life_to_date_net_revenue, 0.00) * c.revenue_share_split) >= c.guaranteed_minimum_royalty THEN (COALESCE(s.life_to_date_net_revenue, 0.00) * c.revenue_share_split)
    ELSE c.guaranteed_minimum_royalty
  END, 2) AS net_amazon_profit_contribution
FROM
  `driiiportfolio.amazon_music_merch.dim_artist_contracts` AS c
LEFT JOIN
  compiled_sales AS s ON c.artist_id = s.artist_id
ORDER BY
  net_amazon_profit_contribution DESC,
  unrecouped_sunk_balance DESC;
