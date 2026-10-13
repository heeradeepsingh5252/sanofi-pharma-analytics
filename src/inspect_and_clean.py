"""Starter data-quality and KPI script for the synthetic portfolio dataset."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

sales = pd.read_csv(DATA / "sales_transactions.csv", parse_dates=["sale_date"])
products = pd.read_csv(DATA / "products.csv")
inventory = pd.read_csv(DATA / "inventory_snapshot.csv")

print("SALES SHAPE:", sales.shape)
print("\nDATA TYPES\n", sales.dtypes)
print("\nMISSING VALUES\n", sales.isna().sum())
print("\nROWS WITH MISSING VALUES:")
print(sales[sales.isna().any(axis=1)])
print("\nDUPLICATE ROWS:", sales.duplicated().sum())
print("\nDUPLICATE SALE IDS:", sales["sale_id"].duplicated().sum())
print("\nDUPLICATE TRANSACTION RECORDS:")

duplicates = sales[
    sales["sale_id"].duplicated(keep=False)
].sort_values("sale_id")

print(duplicates)

# TODO 1: Decide how to handle missing quantity_sold and region; document the decision.
# TODO 2: Remove/resolve duplicate records using a defensible business key.
# TODO 3: Validate product_id joins before creating KPIs.
# TODO 4: Save a cleaned sales table to data/processed/sales_clean.csv.

# Example only: drop fully duplicated rows. Review sale_id duplicates separately first.
sales_clean = sales.drop_duplicates().copy()
# Record missing values before making any changes
print("\nMISSING VALUES AFTER DEDUPLICATION:")
print(sales_clean.isna().sum())

# Keep records with missing region for overall analysis.
# Exclude missing quantity only from quantity-dependent metrics.
sales_with_quantity = sales_clean.dropna(
    subset=["quantity_sold"]
).copy()

print("\nRows retained:", len(sales_clean))
print("Rows with known quantity:", len(sales_with_quantity))
print(
    "Rows with missing region:",
    sales_clean["region"].isna().sum()
)
sales_clean["quantity_sold"] = pd.to_numeric(sales_clean["quantity_sold"], errors="coerce")
print("Rows before cleaning:", len(sales))
print("Rows after removing exact duplicates:",
      len(sales_clean))

print("Duplicate rows remaining:",
      sales_clean.duplicated().sum())

print("Duplicate sale IDs remaining:",
      sales_clean["sale_id"].duplicated().sum())
# Do not silently fill missing values without documenting the business rationale.
sales_clean = sales_clean.dropna(subset=["sale_date", "product_id", "quantity_sold"])
merged = sales_clean.merge(products, on="product_id", how="left", validate="many_to_one", indicator=True)
print("\nJOIN STATUS\n", merged["_merge"].value_counts())
merged = merged.drop(columns=["_merge"])
merged["revenue_inr"] = merged["quantity_sold"] * merged["unit_price_inr"]
merged["estimated_cost_inr"] = merged["quantity_sold"] * merged["unit_cost_inr"]
merged["estimated_gross_profit_inr"] = merged["revenue_inr"] - merged["estimated_cost_inr"]
merged.to_csv(OUT / "sales_enriched.csv", index=False)
print("\nSaved:", OUT / "sales_enriched.csv")
print("Rows after starter cleaning:", len(merged))
print("Revenue (synthetic data):", round(merged["revenue_inr"].sum(), 2))


# Create a local SQLite database
db_path = ROOT / "data" / "pharma_analytics.db"

with sqlite3.connect(db_path) as conn:
    sales_clean.to_sql(
        "sales",
        conn,
        if_exists="replace",
        index=False
    )

    products.to_sql(
        "products",
        conn,
        if_exists="replace",
        index=False
    )

inventory.to_sql(
    "inventory",
    conn,
    if_exists="replace",
    index=False
)


print("SQLite database created:", db_path)
