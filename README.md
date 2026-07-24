# Amazon Music Merch Finance Transformation Engine
An enterprise-grade, end-to-end financial engineering and automated controllership platform that models, aggregates, and simulates commercial risk, supply chain metrics, and royalty recoupment schedules for Amazon Music’s direct-to-fan merchandise ecosystem.
* **Live Interactive Platform:** Google Looker Studio Performance Dashboard (Replace with your secure view-only link)
* **Cloud Architecture:** Google BigQuery Sandbox (Project ID: driiiportfolio)
* **Core Tech Stack:** Vectorized Python Core (Pandas, NumPy), ANSI Google BigQuery SQL, Looker Studio BI semantic layers.

## Business Scenario & Executive Problem Statement

### Corporate Context
The Amazon Music Merch division operates at a unique, high-growth intersection of digital audio streaming and physical/digital retail commerce. Operating as a major tier-one streaming platform, the division leverages Amazon’s broader Prime subscriber base and logistics networks to drive transaction-based merchandise sales directly through artist storefronts and live event touchpoints.

### The Core Business Vulnerability
Due to an expansion of direct-to-fan monetization initiatives, the Culver City media and entertainment hub experienced an operational tracking crisis. Financial analyst bandwidth was severely bottlenecked by highly manual reporting workflows required to bridge disparate ledger databases. This systemic data fragmentation introduced severe vulnerabilities:
* **Unrecouped Royalty Leakage:** High upfront Guaranteed Minimum (GM) royalty commitments were deployed to acquire top-tier talent without automated, transaction-level recoupment tracking loops. This led to massive unrecouped capital deficits hidden on the balance sheet.
* **Supply Chain Blindspots:** Physical fulfillment logs tracking inventory, product damage, and localized holding timelines across warehouses (WH-CULVER, WH-SEATTLE, WH-AUSTIN) were siloed from core financial planning systems. True inventory carrying charges were entirely unaccounted for.
* **Month-End Close Deficiencies:** Excel/VBA reporting engines frequently crashed under growing transaction volumes, causing a 14-day delay in executing month-end closes and stalling operational reviews (OP1/OP2 cycles).

### Quantifiable Fictional Financial Impact
An internal audit isolated a cumulative $4.20 million unhedged financial variance directly attributable to unrecouped talent contracts, a 14-day month-end close lag, and suboptimal pricing execution across core product categories.

## End-to-End Workflow & Architecture Blueprint
The project transforms raw, transactional backend data layers into an automated cloud data warehouse, feeding an interactive decision-support application:

[RAW TRANSACTION DATA]
 ├── Oracle GL Ledger Snapshots (Fixed Upfront Guarantees)
 │     └── Loaded to BigQuery via Python API: `dim_artist_contracts`
 ├── AWS Data Lake / Ingestion Inflows (Raw Sales Transactions)
 │     └── Loaded to BigQuery via Python API: `fact_merch_sales`
 └── Fulfillment System Exports (Warehouse Stagnation Logs)
       └── Loaded to BigQuery via Python API: `fact_inventory_logs`
                │
                ▼
  [AUTOMATED ETL & SCHEMA NORMALIZATION LAYER]
   └── Python Cloud Engine Engine (`WRITE_TRUNCATE` Overwrite Logic)
                │
                ▼
  [CLOUD DATA WAREHOUSE LAYER - GOOGLE BIGQUERY]
   └── Project Partition ID: `driiiportfolio.amazon_music_merch.*`
        ├── View 1: `vw_monthly_financial_summary` (Flattened Margins)
        ├── View 2: `vw_inventory_bottlenecks` (Geocoded Supply Leaks)
        ├── View 3: `vw_artist_deal_recoupment` (Capital Stewardship)
        └── View 4: `waterfall_summary_view` (Vertical Ledger Stack)
                │
                ▼
  [BUSINESS INTELLIGENCE & ENTERPRISE PRESENTATION LAYER]
   └── Looker Studio Dashboard Suite (3-Page Parameter-Driven Engine)
        ├── Page 1: Executive Financial Performance & Margin Control
        ├── Page 2: Physical Supply Chain Metrics & Inventory Health
        └── Page 3: Commercial Deal Valuation & Price Elasticity Modeling

## Technical Deep-Dive: Python Pipeline Engineering

### Phase 2: Exploratory Jupyter Data Validation
The `notebooks/exploratory_financial_review.ipynb` sandbox was deployed prior to the production environment to stress-test data integrity. It programmatically verified that:
* Zero orphan rows or broken foreign keys existed across table joins.
* Statistical distributions aligned directly with commercial categories (e.g., ensuring Tier 3 developing acts were not allocated multi-million dollar Headliner guarantees).
* Relational contract math was benchmarked under real-world parameters before being locked into the production engine.

### Phase 3: Vectorized Production Script
The production pipeline (`scripts/financial_modeling_engine.py`) implements a Tier-Weighted Probability Architecture to eliminate performance bottlenecks. By moving completely away from slow, row-by-row `.map(lambda)` loops, the script executes via fully vectorized NumPy arrays to simulate 60,000 global transactions.
It maps consumer demand realistically (directing 55% of total market volume to Tier 1 Headliners) while natively exporting clean, physical CSV backups and streaming data over an authenticated API directly into Google BigQuery tables using a `WRITE_TRUNCATE` configuration to ensure duplicate-free runs.

## Cloud Warehousing: BigQuery SQL Analytics Suite

### View 1: Monthly Financial Summary View
* **SQL Script Location:** `sql_queries/query1_reconciled_aggregation.sql`
* **Objective:** Aggregates transaction logs, cleanly separating Gross Revenue from Cost of Goods Sold (COGS) and physical handling fees. It solves multi-level aggregation syntax limitations by applying flattened mathematical sums multiplied across single contract split rows to protect against overpayment royalty leakage.

### View 2: Inventory Bottlenecks & Logistics Optimization
* **SQL Script Location:** `sql_queries/query2_variance_inventory_opt.sql`
* **Objective:** Restructures warehouse metrics to calculate annualized inventory turnover velocity and true scrap rate leakages. It injects explicit geographic strings (e.g., "Culver City, CA", "Seattle, WA") to allow downstream Looker Studio map visualization mapping pins to anchor natively without geocoding drops.

### View 3: Deal Valuation & Capital Stewardship Engine
* **SQL Script Location:** `sql_queries/query3_deal_valuation_npv.sql`
* **Objective:** Operates as a master contract grading ledger. It compares upfront cash commitments against accrued split earnings, dynamically tagging recoupment statuses and calculating unrecouped sunk balances to give leadership immediate visibility into portfolio risk.

## Business Intelligence Layer: Looker Studio Blueprint
The visual dashboard application is constructed across a 3-Page Narrative Architecture using a stylized palette of Dark Slate Grey (`#111625`) and Amazon Orange (`#FF9900`) for high executive clarity.

### Page 1: Executive Financial Performance & Margin Control
* **Global KPI Scorecards:** Houses high-impact metrics tracking global portfolio revenues alongside overall sunk cost risks.
* **Financial Breakdown Waterfall Chart:** Connected to `waterfall_summary_view`. Configured via an explicit ascending index sort to force a clean left-to-right cascade from top-line Gross Revenue, through operational deductions, landing cleanly on the Net Amazon Profit Position.
* **Blended Gross Margin % vs. 250 BPS Goal:** An industry-standard Bullet Chart mapped to a fixed target value threshold of 0.604 (60.4%). It charts actual margin progress over shaded contextual background ranges to visualize performance against the 250 basis point optimization mandate.

### Page 2: Physical Supply Chain Metrics & Inventory Health
* **Warehouse Performance Map:** A native Google Maps visual connecting to geo_location dimensions. It maps facility performance, where bubble sizes represent total carrying cost burdens, and color shades isolate exact scrap leakage trends.
* **Inventory Velocity Scatter Plot Matrix:** Configured with a display limit of 150 bubbles to prevent data truncation warnings. It maps `average_days_held` (X-Axis) against `inventory_turnover_velocity` (Y-Axis) at an average aggregation grain (AVG). This exposes unoptimized dead stock dragging down margins in the bottom-right quadrant.
* **Tabular Performance Grid Ledger:** A detailed operational ledger displaying warehouse metrics sorted descending by `cumulative_carrying_cost` to float worst-performing facilities instantly to the top for managerial review.

### Page 3: Commercial Deal Valuation & Price Elasticity Modeling
* **Interactive Simulation Matrix Table:** Integrates custom input box controls for volume and retail price modifiers (`p_forecast_volume_modifier` and `p_forecast_price_modifier`). It utilizes calculated metric formulas to display dynamic, simulated margin outcomes in real-time.
* **Net Amazon Profit Bar Chart:** Connected to a unified, parameter-aware Looker Studio blended data source (`Blended_Deal_Simulation`). This joins transactional sales with fixed contract dimensions, forcing the bars to respond dynamically to the input sliders and displaying side-by-side clustered comparisons between upfront capital commitments and dynamic net profit contribution columns across all three artist tiers.
* **Recoupment Status Distribution Chart:** A donut visualization plotting a precise split of 98.0% Unrecouped vs. 2.0% Recouped positions. This realistic distribution matches real-world entertainment venture-capital profiles, where a single successful contract in a conservative tier (Artist 25) achieves recoupment, while high-liability headliner contracts generate long-term structural deficits over short operational windows.

## Enterprise Success Metrics & KPI Framework
To ensure maximum controllership and alignment with Amazon’s leadership criteria, project execution is weighted against five distinct corporate scorecard metrics:
* **Financial Core Metrics (40% Weight):** Evaluates forecast-to-actual variance performance, blended gross profit margins, and net portfolio growth vectors.
* **Operational Efficiency Metrics (25% Weight):** Tracks the systematic compression of the month-end accounting close timeline, deal evaluation turnaround speed, and inventory carrying cost reduction.
* **Data Quality Metrics (15% Weight):** Ensures 100% audit compliance, zero ledger reconciliation variances, and error-free royalty processing workflows.
* **Engineering Productivity Metrics (10% Weight):** Measures total volume of automated data pipelines established and commercial contracts programmatically evaluated.
* **Strategic Alignment Metrics (10% Weight):** Evaluates successful cross-functional continuous improvement execution and business development partner enablement.

```
