import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "database" / "retail_sales.db"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)

if not DATABASE.exists():
    raise FileNotFoundError("Run generate_data.py before analyze.py")

with sqlite3.connect(DATABASE) as connection:
    sales = pd.read_sql_query("""
        SELECT f.order_id, f.order_date, f.customer_id, f.product_id,
               f.quantity, f.discount, f.sales, f.profit,
               c.segment, c.region, p.category, p.subcategory, p.product_name
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        JOIN dim_product p ON f.product_id = p.product_id
    """, connection)

sales["order_date"] = pd.to_datetime(sales["order_date"])
sales["year"] = sales["order_date"].dt.year
sales["month"] = sales["order_date"].dt.to_period("M").astype(str)

monthly = sales.groupby("month", as_index=False)[["sales", "profit"]].sum()
category = sales.groupby("category", as_index=False)[["sales", "profit"]].sum().sort_values("sales", ascending=False)
region = sales.groupby("region", as_index=False)[["sales", "profit"]].sum().sort_values("sales", ascending=False)
segment = sales.groupby("segment", as_index=False)[["sales", "profit"]].sum().sort_values("sales", ascending=False)

monthly.to_csv(OUTPUT / "monthly_performance.csv", index=False)
category.to_csv(OUTPUT / "category_performance.csv", index=False)
region.to_csv(OUTPUT / "region_performance.csv", index=False)
segment.to_csv(OUTPUT / "segment_performance.csv", index=False)

plt.style.use("seaborn-v0_8-whitegrid")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["month"], monthly["sales"], marker="o", color="#2563eb", label="Sales")
ax.plot(monthly["month"], monthly["profit"], marker="o", color="#16a34a", label="Profit")
ax.set_title("Monthly Sales and Profit")
ax.set_xlabel("Month")
ax.set_ylabel("Amount")
ax.tick_params(axis="x", rotation=75)
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT / "monthly_trend.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(category["category"], category["sales"], color="#7c3aed")
ax.invert_yaxis()
ax.set_title("Sales by Product Category")
ax.set_xlabel("Sales")
fig.tight_layout()
fig.savefig(OUTPUT / "category_sales.png", dpi=150)
plt.close(fig)

print("Analysis complete")
print("Key metrics")
print({
    "orders": len(sales),
    "sales": round(sales["sales"].sum(), 2),
    "profit": round(sales["profit"].sum(), 2),
    "profit_margin": round(sales["profit"].sum() / sales["sales"].sum(), 4),
})
print(f"Outputs: {OUTPUT}")
