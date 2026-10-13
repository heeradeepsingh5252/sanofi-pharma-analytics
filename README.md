# Pharmaceutical Sales & Inventory Analytics (Synthetic Portfolio Project)

## Important context
This is a portfolio project using **synthetic, fictional data**. It is not Sanofi internal data and is not affiliated with or endorsed by Sanofi. Product names are fictional placeholders, not real medicines. Do not present synthetic results as real business findings.

## Business problem
A fictional pharmaceutical distributor wants to understand product sales, revenue, regional performance, sales channels, and inventory risk. The analyst must clean source data, answer business questions with SQL/Python, and build an interactive Power BI report.

## Dataset files
- `data/raw/sales_transactions.csv`: transaction-level sales; includes two duplicated records and a small number of missing values intentionally for cleaning practice.
- `data/raw/products.csv`: fictional product dimension with category, price, cost and reorder threshold.
- `data/raw/inventory_snapshot.csv`: synthetic regional stock snapshot for inventory-risk analysis.

## Recommended workflow
1. Inspect all three CSV files and document row counts, data types, nulls, duplicates and key uniqueness.
2. Clean the transaction data: parse dates, investigate duplicate `sale_id` values/rows, handle missing quantity and region transparently, and validate joins.
3. Join sales to products and derive revenue, cost and gross profit.
4. Load the cleaned tables into a local SQL database (SQLite is enough) and solve the questions in `sql/analysis_questions.sql`.
5. Use Python/Pandas for quality checks and exploratory analysis.
6. Build a Power BI report with overview, product/region performance, and inventory pages.
7. Write a one-page executive summary with findings, limitations and recommendations.
8. Practice explaining each decision, especially data cleaning and KPI definitions.

## KPIs
- Revenue = quantity sold × unit price
- Estimated cost = quantity sold × unit cost
- Estimated gross profit = revenue − estimated cost
- Gross margin % = gross profit ÷ revenue
- Inventory coverage proxy = closing stock units ÷ average daily units sold (only if periods are comparable and the assumptions are documented)
- Reorder flag = closing stock units < reorder level units

## Suggested Power BI pages
1. Executive Overview: revenue, units sold, estimated gross profit, transaction count, monthly trend.
2. Product & Channel: category/product rankings, channel contribution, product-level margin.
3. Region Performance: region comparison and monthly trends.
4. Inventory: closing stock vs reorder level, products/regions flagged for review.

## Interview presentation (90 seconds)
"I built an end-to-end analytics project using fictional pharmaceutical sales and inventory data. I profiled and cleaned transaction data, joined sales to product attributes, defined revenue and estimated gross-profit KPIs, used SQL to answer business questions, and designed a Power BI dashboard for product, channel, regional and inventory performance. I documented assumptions and data limitations so that the report is useful without overstating what the data can prove."

## Folder guide
- `data/raw`: source CSVs (keep unchanged)
- `data/processed`: cleaned/derived data
- `notebooks`: exploratory notebook(s) you create
- `sql`: SQL analysis queries
- `src`: reusable Python scripts
- `powerbi`: save the `.pbix` report here
- `docs`: data dictionary, QA log, insights and screenshots
