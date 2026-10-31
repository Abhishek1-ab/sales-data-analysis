# Retail Sales Data Analysis Project

A portfolio-ready end-to-end data analysis project using Python, SQL, and Power BI.

## Business goal
Analyze retail sales, profit, customer segments, regions, products, discounts, and monthly trends.

## Project contents

```text
├── generate_data.py       # Creates synthetic retail data and SQLite database
├── analyze.py             # Runs Python analysis and exports charts/summary CSVs
├── main.ipynb             # Exploratory notebook
├── data/                  # Customer, product, order, and date CSV files
├── database/              # SQLite retail_sales.db
├── sql/analysis_queries.sql
├── outputs/               # Charts and aggregated analysis tables
├── requirements.txt
└── README.md
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python generate_data.py
python analyze.py
```

## SQL workflow

Open `database/retail_sales.db` with DB Browser for SQLite or any SQLite client and execute queries from `sql/analysis_queries.sql`.

## Power BI workflow

1. Open Power BI Desktop.
2. Select **Get data → Text/CSV**.
3. Load the four files in the `data` folder.
4. Use `orders.csv` as the fact table and join it to:
   - `orders.customer_id` → `customers.customer_id`
   - `orders.product_id` → `products.product_id`
5. Join `orders.order_date` to `dates.date`.
6. Create these measures in DAX:

```DAX
Total Sales = SUM(orders[sales])
```

```DAX
Total Profit = SUM(orders[profit])
```

```DAX
Profit Margin % = DIVIDE([Total Profit], [Total Sales])
```

```DAX
Average Order Value = DIVIDE([Total Sales], DISTINCTCOUNT(orders[order_id]))
```

## Recommended dashboard pages

- Executive overview: KPI cards, monthly trend, category performance, region map
- Product performance: top products, category and subcategory analysis
- Customer analysis: customer segments, regional breakdown, sales distribution
- Discount analysis: sales and profit by discount level

## Key decisions and findings

Using the generated dataset, the current analysis contains 5,000 orders, approximately $3.14 million in total sales, and approximately $995,666 in total profit (31.76% profit margin). Use the category and region CSV outputs or refresh the analysis after changing the random seed or parameters to update the findings.

## Push to GitHub

```powershell
git init
git add .
git commit -m "Add retail sales end-to-end data analysis project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/RETAIL-SALES-ANALYSIS.git
git push -u origin main
```
