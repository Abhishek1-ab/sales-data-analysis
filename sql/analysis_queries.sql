-- Retail sales analysis queries

-- 1. Overall business KPIs
SELECT
    COUNT(*) AS total_orders,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM fact_sales;

-- 2. Monthly sales trend
SELECT
    substr(order_date, 1, 7) AS year_month,
    SUM(sales) AS sales,
    SUM(profit) AS profit
FROM fact_sales
GROUP BY substr(order_date, 1, 7)
ORDER BY year_month;

-- 3. Category performance
SELECT
    p.category,
    SUM(f.sales) AS sales,
    SUM(f.profit) AS profit,
    ROUND(100.0 * SUM(f.profit) / NULLIF(SUM(f.sales), 0), 2) AS margin_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY sales DESC;

-- 4. Regional performance
SELECT
    c.region,
    SUM(f.sales) AS sales,
    SUM(f.profit) AS profit,
    COUNT(DISTINCT c.customer_id) AS customers
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.region
ORDER BY sales DESC;

-- 5. Top 10 products
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales) AS sales,
    SUM(f.profit) AS profit
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY sales DESC
LIMIT 10;

-- 6. Customer segment analysis
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    SUM(f.sales) AS sales,
    SUM(f.profit) AS profit,
    ROUND(AVG(f.sales), 2) AS average_order_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY sales DESC;

-- 7. Discount impact on profitability
SELECT
    discount,
    COUNT(*) AS orders,
    SUM(sales) AS sales,
    SUM(profit) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS margin_pct
FROM fact_sales
GROUP BY discount
ORDER BY discount;
