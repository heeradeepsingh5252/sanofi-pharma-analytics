# Data Dictionary

## sales_transactions.csv
- sale_id: synthetic transaction identifier
- sale_date: transaction date in 2025
- product_id: foreign key to products
- region: sales region
- sales_channel: retail pharmacy, hospital, online pharmacy or distributor
- quantity_sold: units sold; contains a small number of missing values for practice

## products.csv
- product_id: product key
- product_name: fictional product label
- category: fictional product category
- unit_price_inr: synthetic selling price per unit
- unit_cost_inr: synthetic unit cost used for estimated profit calculations
- reorder_level_units: stock threshold used in the sample inventory table

## inventory_snapshot.csv
- product_id, region: composite key for product/region snapshot
- opening_stock_units: synthetic starting stock
- received_units: synthetic stock received during period
- units_sold_period: synthetic units sold during period
- closing_stock_units: synthetic closing stock
- reorder_level_units: threshold for review

## Quality caveats
Synthetic transactions include intentional duplicate rows and missing values. Product price/cost values are illustrative. The inventory snapshot is independently generated, so do not claim that it reconciles exactly to the transaction table. In a real project, reconcile inventory movement and sales for matching products, regions and periods before calculating stock coverage.
