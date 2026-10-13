-- Start with these questions. Run against a cleaned sales table joined to products.
-- Adapt table/column names to your SQLite schema.

-- 1. Monthly revenue and units sold
SELECT strftime('%Y-%m', sale_date) AS month,
       SUM(quantity_sold * unit_price_inr) AS revenue_inr,
       SUM(quantity_sold) AS units_sold
FROM sales_clean
JOIN products USING (product_id)
GROUP BY month
ORDER BY month;

-- 2. Top 5 products by revenue
SELECT p.product_name,
       SUM(s.quantity_sold * p.unit_price_inr) AS revenue_inr
FROM sales_clean s
JOIN products p USING (product_id)
GROUP BY p.product_name
ORDER BY revenue_inr DESC
LIMIT 5;

-- 3. Revenue by region and channel
SELECT s.region, s.sales_channel,
       SUM(s.quantity_sold * p.unit_price_inr) AS revenue_inr
FROM sales_clean s
JOIN products p USING (product_id)
GROUP BY s.region, s.sales_channel
ORDER BY revenue_inr DESC;

-- 4. Gross profit and gross margin by category
SELECT p.category,
       SUM(s.quantity_sold * p.unit_price_inr) AS revenue_inr,
       SUM(s.quantity_sold * p.unit_cost_inr) AS estimated_cost_inr,
       SUM(s.quantity_sold * (p.unit_price_inr - p.unit_cost_inr)) AS estimated_gross_profit_inr,
       100.0 * SUM(s.quantity_sold * (p.unit_price_inr - p.unit_cost_inr))
         / NULLIF(SUM(s.quantity_sold * p.unit_price_inr), 0) AS gross_margin_pct
FROM sales_clean s
JOIN products p USING (product_id)
GROUP BY p.category
ORDER BY estimated_gross_profit_inr DESC;

-- 5. Inventory below reorder level
SELECT i.region, p.product_name, i.closing_stock_units, i.reorder_level_units
FROM inventory_snapshot i
JOIN products p USING (product_id)
WHERE i.closing_stock_units < i.reorder_level_units
ORDER BY (i.reorder_level_units - i.closing_stock_units) DESC;

-- 6. Check duplicated transaction IDs
SELECT sale_id, COUNT(*) AS records
FROM sales_raw
GROUP BY sale_id
HAVING COUNT(*) > 1;

SELECT
    product_id,
    SUM(quantity_sold) AS total_quantity_sold
FROM sales
GROUP BY product_id
ORDER BY total_quantity_sold DESC;