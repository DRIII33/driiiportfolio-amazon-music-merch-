import pandas as pd
import numpy as np
import logging
import os # Import the os module

# Configure enterprise logging framework
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_financial_pipeline():
    logging.info("Initializing Amazon Music Merch Financial Modeling Pipeline.")
    np.random.seed(42)

    # Create the 'data' directory if it doesn't exist
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}/")

    # -------------------------------------------------------------------------
    # 1. DATA GENERATION ENGINE (FULLY VECTORIZED)
    # -------------------------------------------------------------------------
    num_artists = 50
    logging.info(f"Generating dimensional infrastructure for {num_artists} artist contracts.")

    # Vectorized generation of dim_artist_contracts
    artist_ids = np.char.add("ART-", np.char.zfill(np.arange(1, num_artists + 1).astype(str), 4))
    tiers = np.random.choice(
        ['Tier 1 (Headliner)', 'Tier 2 (Mid-Level)', 'Tier 3 (Developing)'],
        size=num_artists,
        p=[0.1, 0.3, 0.6]
    )

    # Precise conditional mapping for Guaranteed Minimum options via numpy
    guarantees = np.where(tiers == 'Tier 1 (Headliner)', np.random.randint(500000, 2000000, num_artists),
                 np.where(tiers == 'Tier 2 (Mid-Level)', np.random.randint(50000, 300000, num_artists),
                          np.random.randint(5000, 25000, num_artists)))

    rev_shares = np.random.uniform(0.15, 0.40, num_artists)

    dim_artist_contracts = pd.DataFrame({
        'artist_id': artist_ids,
        'artist_name': np.char.add("Artist ", np.arange(1, num_artists + 1).astype(str)),
        'artist_tier': tiers,
        'guaranteed_minimum_royalty': guarantees.astype(float),
        'revenue_share_split': np.round(rev_shares, 4),
        'contract_start_date': pd.Timestamp('2025-01-01'),
        'contract_end_date': pd.Timestamp('2027-12-31')
    })

    # =============================================================================
    # REVISED TRANSACTION GENERATION LAYER (PASTE INTO YOUR SCRIPT CORE)
    # =============================================================================
    num_sales = 60000
    logging.info(f"Generating {num_sales} high-volume tier-weighted transactions.")
    start_time = pd.Timestamp('2025-01-01')
    max_hours = int((pd.Timestamp('2026-07-01') - start_time).total_seconds() / 3600)

    random_hours = np.random.randint(0, max_hours, num_sales)
    sample_timestamps = start_time + pd.to_timedelta(random_hours, unit='h')

    categories = ['Vinyl', 'Apparel', 'Custom Accessories']
    channels = ['Digital Storefront', 'Physical Tour Fulfillment']

    # Extract structural IDs mapped directly to their generated contract tiers
    t1_ids = dim_artist_contracts.loc[dim_artist_contracts['artist_tier'] == 'Tier 1 (Headliner)', 'artist_id'].values
    t2_ids = dim_artist_contracts.loc[dim_artist_contracts['artist_tier'] == 'Tier 2 (Mid-Level)', 'artist_id'].values
    t3_ids = dim_artist_contracts.loc[dim_artist_contracts['artist_tier'] == 'Tier 3 (Developing)', 'artist_id'].values

    # Establish a real-world consumer demand distribution
    all_generated_artist_ids = []
    for _ in range(num_sales):
        tier_choice = np.random.choice(['T1', 'T2', 'T3'], p=[0.55, 0.30, 0.15]) # Headliners command 55% of market volume
        if tier_choice == 'T1' and len(t1_ids) > 0:
            all_generated_artist_ids.append(np.random.choice(t1_ids))
        elif tier_choice == 'T2' and len(t2_ids) > 0:
            all_generated_artist_ids.append(np.random.choice(t2_ids))
        elif tier_choice == 'T3' and len(t3_ids) > 0: # Ensure T3 is handled if only T1 and T2 are empty or if it's explicitly chosen
            all_generated_artist_ids.append(np.random.choice(t3_ids))
        else: # Fallback in case a tier list is unexpectedly empty
            all_generated_artist_ids.append(np.random.choice(artist_ids)) # Choose from all artists if a specific tier is empty

    fact_merch_sales = pd.DataFrame({
        'transaction_id': np.char.add("TXN-", np.char.zfill(np.arange(1, num_sales + 1).astype(str), 6)),
        'timestamp': sample_timestamps,
        'artist_id': all_generated_artist_ids,
        'product_category': np.random.choice(categories, num_sales, p=[0.3, 0.5, 0.2]),
        'channel': np.random.choice(channels, num_sales, p=[0.8, 0.2]),
        'units_sold': np.random.randint(1, 5, num_sales)
    })

    # High-performance static index mapping (Eliminates loops/lambdas)
    retail_map = {'Vinyl': 35.00, 'Apparel': 45.00, 'Custom Accessories': 20.00}
    cogs_map = {'Vinyl': 12.00, 'Apparel': 15.00, 'Custom Accessories': 5.00}
    shipping_map = {'Vinyl': 4.50, 'Apparel': 3.50, 'Custom Accessories': 2.00}

    fact_merch_sales['unit_retail_price'] = fact_merch_sales['product_category'].map(retail_map)
    fact_merch_sales['unit_manufacturing_cost'] = fact_merch_sales['product_category'].map(cogs_map)
    fact_merch_sales['shipping_fees'] = fact_merch_sales['product_category'].map(shipping_map)

    # Vectorized generation of fact_inventory_logs
    num_logs = 500
    logging.info(f"Generating {num_logs} relational physical inventory logs.")
    start_date = pd.Timestamp('2025-01-01')
    max_days = (pd.Timestamp('2026-07-01') - start_date).days
    random_days = np.random.randint(0, max_days, num_logs)

    fact_inventory_logs = pd.DataFrame({
        'log_id': np.char.add("LOG-", np.char.zfill(np.arange(1, num_logs + 1).astype(str), 5)),
        'log_date': start_date + pd.to_timedelta(random_days, unit='D'),
        'warehouse_id': np.random.choice(['WH-CULVER', 'WH-SEATTLE', 'WH-AUSTIN'], num_logs),
        'artist_id': np.random.choice(artist_ids, num_logs),
        'units_received': np.random.randint(100, 5000, num_logs),
        'units_damaged': np.random.randint(0, 50, num_logs),
        'days_in_storage': np.random.randint(15, 120, num_logs),
        'daily_unit_holding_cost': 0.02
    })

    # -------------------------------------------------------------------------
    # 2. FINANCIAL ANALYSIS ENGINE
    # -------------------------------------------------------------------------
    logging.info("Executing relational financial calculations and recoupment analysis.")

    # Core margins execution
    fact_merch_sales['gross_revenue'] = fact_merch_sales['units_sold'] * fact_merch_sales['unit_retail_price']
    fact_merch_sales['total_cogs'] = fact_merch_sales['units_sold'] * fact_merch_sales['unit_manufacturing_cost']
    fact_merch_sales['net_revenue'] = (
        fact_merch_sales['gross_revenue'] -
        fact_merch_sales['total_cogs'] -
        (fact_merch_sales['units_sold'] * fact_merch_sales['shipping_fees'])
    )

    # Aggregate net revenue by individual artist
    artist_sales = fact_merch_sales.groupby('artist_id', as_index=False)['net_revenue'].sum()
    royalty_analysis = pd.merge(artist_sales, dim_artist_contracts, on='artist_id')

    # Royalty settlement logic mapping
    royalty_analysis['earned_royalties'] = royalty_analysis['net_revenue'] * royalty_analysis['revenue_share_split']
    royalty_analysis['is_recouped'] = royalty_analysis['earned_royalties'] >= royalty_analysis['guaranteed_minimum_royalty']
    royalty_analysis['net_payout_liability'] = np.maximum(
        royalty_analysis['guaranteed_minimum_royalty'],
        royalty_analysis['earned_royalties']
    )

    # Calculate physical supply chain leakage
    fact_inventory_logs['total_carrying_cost'] = (
        fact_inventory_logs['units_received'] *
        fact_inventory_logs['days_in_storage'] *
        fact_inventory_logs['daily_unit_holding_cost']
    )

    # -------------------------------------------------------------------------
    # 3. 12-MONTH ROLLING FORECAST SIMULATION (250 BPS TARGET TARGET)
    # -------------------------------------------------------------------------
    logging.info("Modeling 12-Month forward rolling margin targets.")
    current_gross_revenue = fact_merch_sales['gross_revenue'].sum()
    current_cogs = fact_merch_sales['total_cogs'].sum()
    current_margin_pct = (current_gross_revenue - current_cogs) / current_gross_revenue

    # Pricing elasticity model inputs: 8% retail increase leading to a 5% drop in product volume
    forecast_volume_modifier = 0.95
    forecast_price_modifier = 1.08

    projected_gross_revenue = current_gross_revenue * forecast_price_modifier * forecast_volume_modifier
    projected_cogs = current_cogs * forecast_volume_modifier
    projected_margin_pct = (projected_gross_revenue - projected_cogs) / projected_gross_revenue

    # -------------------------------------------------------------------------
    # 4. EXECUTIVE CONSOLE GENERATION
    # -------------------------------------------------------------------------
    print("\n" + "="*57)
    print("AMAZON MUSIC MERCH FINANCE: EXECUTIVE SUMMARY (PRODUCTION)")
    print("="*57)
    print(f"Total Gross Revenue Generated : ${current_gross_revenue:,.2f}")
    print(f"Total Cost of Goods Sold      : ${current_cogs:,.2f}")
    print(f"Blended Base Gross Margin     : {current_margin_pct:.2%}")
    print(f"Total Inventory Carrying Cost : ${fact_inventory_logs['total_carrying_cost'].sum():,.2f}")
    print("-"*57)
    print("ROYALTY RECOUPMENT STATUS & LIABILITY TRACKING:")
    print(f"Guaranteed Minimums Deployed  : ${royalty_analysis['guaranteed_minimum_royalty'].sum():,.2f}")
    print(f"Successfully Recouped Artists : {royalty_analysis['is_recouped'].sum()} / {num_artists}")

    unrecouped_mask = ~royalty_analysis['is_recouped']
    sunk_cost_risk = (
        royalty_analysis.loc[unrecouped_mask, 'guaranteed_minimum_royalty'] -
        royalty_analysis.loc[unrecouped_mask, 'earned_royalties']
    ).sum()
    print(f"Unrecouped Sunk Cost Balance  : ${sunk_cost_risk:,.2f}")
    print("-"*57)
    print("STRATEGIC FORECAST SIMULATION (250 BPS MARGIN EXPANSION):")
    print(f"Projected Target Gross Margin : {projected_margin_pct:.2%}")
    margin_bps_delta = (projected_margin_pct - current_margin_pct) * 10000
    print(f"Modeled Structural Variance  : +{margin_bps_delta:,.0f} bps")
    incremental_profit = (projected_gross_revenue - projected_cogs) - (current_gross_revenue - current_cogs)
    print(f"Projected Incremental Profit  : ${incremental_profit:,.2f}")
    print("="*57 + "\n")

    # =============================================================================
    # 3.5 EXPORT ENGINE (ADD THIS BLOCK TO GENERATE THE PHYSICAL FILES)
    # =============================================================================
    logging.info("Writing clean synthetic databases to physical CSV files.")

    # index=False prevents Pandas from creating an un-named row index column
    dim_artist_contracts.to_csv('data/raw_artist_contracts.csv', index=False)
    fact_merch_sales.to_csv('data/raw_merch_sales.csv', index=False)
    fact_inventory_logs.to_csv('data/raw_inventory_logs.csv', index=False)

    logging.info("CSV generation complete. Files exported to the data/ directory.")

    logging.info("Pipeline executed successfully with zero fatal errors.")

    return royalty_analysis, dim_artist_contracts, fact_merch_sales, fact_inventory_logs

if __name__ == "__main__":
    # The if __name__ == "__main__" block will not be executed when the notebook is run top-to-bottom.
    # We need to call the function explicitly and assign its return values globally.
    pass
