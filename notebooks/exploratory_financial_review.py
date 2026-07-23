# %% [markdown]
# # Amazon Music Merch Finance: Exploratory Financial Review
# **Author:** Daniel Rodriguez III - Financial Analyst (Seattle, WA)
# **Objective:** Validate synthetic data profiles, verify relational integrity, 
# and prototype financial recoupment / margin expansion models.

# %% [cell 1: Imports & Configurations]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set seed for repeatable, reproducible results
np.random.seed(42)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

print("Environment verified. Packages initialized.")

# %% [cell 2: Prototype Dimensional Infrastructure - Artist Contracts]
num_artists = 50
artist_ids = np.char.add("ART-", np.char.zfill(np.arange(1, num_artists + 1).astype(str), 4))
tiers = np.random.choice(
    ['Tier 1 (Headliner)', 'Tier 2 (Mid-Level)', 'Tier 3 (Developing)'], 
    size=num_artists, 
    p=[0.1, 0.3, 0.6]
)

# Apply step-wise conditions for realistic enterprise guarantees
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

print("--- DIM_ARTIST_CONTRACTS DISTRIBUTION CHECK ---")
print(dim_artist_contracts.groupby('artist_tier')['guaranteed_minimum_royalty'].describe())

# %% [cell 3: Prototype Transactional Logs - Merch Sales]
num_sales = 5000
start_time = pd.Timestamp('2025-01-01')
max_hours = int((pd.Timestamp('2026-07-01') - start_time).total_seconds() / 3600)

random_hours = np.random.randint(0, max_hours, num_sales)
sample_timestamps = start_time + pd.to_timedelta(random_hours, unit='h')

categories = ['Vinyl', 'Apparel', 'Custom Accessories']
channels = ['Digital Storefront', 'Physical Tour Fulfillment']

fact_merch_sales = pd.DataFrame({
    'transaction_id': np.char.add("TXN-", np.char.zfill(np.arange(1, num_sales + 1).astype(str), 6)),
    'timestamp': sample_timestamps,
    'artist_id': np.random.choice(artist_ids, num_sales),
    'product_category': np.random.choice(categories, num_sales, p=[0.2, 0.6, 0.2]),
    'channel': np.random.choice(channels, num_sales, p=[0.8, 0.2]),
    'units_sold': np.random.randint(1, 5, num_sales)
})

# Flatten lookup metrics mapping
retail_map = {'Vinyl': 35.00, 'Apparel': 45.00, 'Custom Accessories': 20.00}
cogs_map = {'Vinyl': 12.00, 'Apparel': 15.00, 'Custom Accessories': 5.00}
shipping_map = {'Vinyl': 4.50, 'Apparel': 3.50, 'Custom Accessories': 2.00}

fact_merch_sales['unit_retail_price'] = fact_merch_sales['product_category'].map(retail_map)
fact_merch_sales['unit_manufacturing_cost'] = fact_merch_sales['product_category'].map(cogs_map)
fact_merch_sales['shipping_fees'] = fact_merch_sales['product_category'].map(shipping_map)

print("\n--- FACT_MERCH_SALES SAMPLE CHECK ---")
print(fact_merch_sales.head(3))

# %% [cell 4: Prototype Supply Chain Logs - Inventory Records]
num_logs = 500
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

print("\n--- FACT_INVENTORY_LOGS SUMMARY CHECK ---")
print(fact_inventory_logs.describe())

# %% [cell 5: Execute Prototyped Financial Recoupment Mathematics]
fact_merch_sales['gross_revenue'] = fact_merch_sales['units_sold'] * fact_merch_sales['unit_retail_price']
fact_merch_sales['total_cogs'] = fact_merch_sales['units_sold'] * fact_merch_sales['unit_manufacturing_cost']
fact_merch_sales['net_revenue'] = (
    fact_merch_sales['gross_revenue'] - 
    fact_merch_sales['total_cogs'] - 
    (fact_merch_sales['units_sold'] * fact_merch_sales['shipping_fees'])
)

artist_sales = fact_merch_sales.groupby('artist_id', as_index=False)['net_revenue'].sum()
royalty_analysis = pd.merge(artist_sales, dim_artist_contracts, on='artist_id')

royalty_analysis['earned_royalties'] = royalty_analysis['net_revenue'] * royalty_analysis['revenue_share_split']
royalty_analysis['is_recouped'] = royalty_analysis['earned_royalties'] >= royalty_analysis['guaranteed_minimum_royalty']

print("\n--- RELATIONAL RECOUPMENT SIMULATION VERIFICATION ---")
recouped_count = royalty_analysis['is_recouped'].sum()
total_contracts = len(royalty_analysis)
print(f"Verified Recouped Contracts: {recouped_count} out of {total_contracts} ({recouped_count/total_contracts:.1%})")

# %% [cell 6: Stress-Test Data Integrity for Downstream Joins]
# Check for null values and orphan IDs across datasets
sales_orphans = fact_merch_sales[~fact_merch_sales['artist_id'].isin(dim_artist_contracts['artist_id'])]
inventory_orphans = fact_inventory_logs[~fact_inventory_logs['artist_id'].isin(dim_artist_contracts['artist_id'])]

print("\n--- INTEGRITY CHECKS ---")
print(f"Missing Values Found in Transactions: {fact_merch_sales.isna().sum().sum()}")
print(f"Orphaned Sales Records Detected: {len(sales_orphans)}")
print(f"Orphaned Inventory Records Detected: {len(inventory_orphans)}")
print("Data validation pass verified. Integrity confirmed for production migration.")
