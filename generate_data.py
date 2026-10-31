import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATABASE_DIR = ROOT / "database"
DATA_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)

regions = ["North", "South", "East", "West"]
segments = ["Consumer", "Corporate", "Home Office"]
categories = {
    "Technology": ["Laptop", "Tablet", "Monitor", "Phone", "Accessories"],
    "Furniture": ["Chair", "Desk", "Table", "Shelf", "Lamp"],
    "Office Supplies": ["Paper", "Storage", "Writing", "Binders", "Art Supplies"],
}

# Dimension: products
product_rows = []
product_id = 1
for category, names in categories.items():
    for subcategory in names:
        for variant in range(1, 6):
            base_price = {"Technology": 420, "Furniture": 180, "Office Supplies": 35}[category]
            price = round(max(10, np.random.normal(base_price, base_price * 0.18)), 2)
            unit_cost = round(price * np.random.uniform(0.55, 0.75), 2)
            product_rows.append({
                "product_id": product_id,
                "product_name": f"{subcategory} {variant}",
                "category": category,
                "subcategory": subcategory,
                "unit_price": price,
                "unit_cost": unit_cost,
            })
            product_id += 1
products = pd.DataFrame(product_rows)

# Dimension: customers
customer_rows = []
for customer_id in range(1, 501):
    customer_rows.append({
        "customer_id": customer_id,
        "customer_name": f"Customer {customer_id:03d}",
        "segment": np.random.choice(segments, p=[0.50, 0.30, 0.20]),
        "region": np.random.choice(regions),
    })
customers = pd.DataFrame(customer_rows)

# Fact: orders
order_rows = []
start = pd.Timestamp("2023-01-01")
end = pd.Timestamp("2025-12-31")
days = (end - start).days
for order_id in range(1, 5001):
    order_date = start + pd.Timedelta(days=int(np.random.randint(0, days + 1)))
    customer = customers.iloc[np.random.randint(0, len(customers))]
    product = products.iloc[np.random.randint(0, len(products))]
    quantity = int(np.clip(np.random.poisson(2.2) + 1, 1, 8))
    discount = float(np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.35, 0.25, 0.20, 0.15, 0.05]))
    sales = round(product["unit_price"] * quantity * (1 - discount), 2)
    profit = round(sales - (product["unit_cost"] * quantity), 2)
    ship_days = int(np.clip(np.random.normal(4, 1.5), 1, 9))
    ship_date = order_date + pd.Timedelta(days=ship_days)
    order_rows.append({
        "order_id": order_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "ship_date": ship_date.strftime("%Y-%m-%d"),
        "customer_id": int(customer["customer_id"]),
        "product_id": int(product["product_id"]),
        "quantity": quantity,
        "discount": discount,
        "sales": sales,
        "profit": profit,
    })
orders = pd.DataFrame(order_rows)

# Date dimension
dates = pd.DataFrame({"date": pd.date_range("2023-01-01", "2025-12-31", freq="D")})
dates["year"] = dates["date"].dt.year
dates["quarter"] = "Q" + dates["date"].dt.quarter.astype(str)
dates["month"] = dates["date"].dt.month
dates["month_name"] = dates["date"].dt.strftime("%B")
dates["date"] = dates["date"].dt.strftime("%Y-%m-%d")

# Export CSV files for Power BI
customers.to_csv(DATA_DIR / "customers.csv", index=False)
products.to_csv(DATA_DIR / "products.csv", index=False)
orders.to_csv(DATA_DIR / "orders.csv", index=False)
dates.to_csv(DATA_DIR / "dates.csv", index=False)

# Build SQLite star schema for SQL analysis
with sqlite3.connect(DATABASE_DIR / "retail_sales.db") as connection:
    customers.to_sql("dim_customer", connection, if_exists="replace", index=False)
    products.to_sql("dim_product", connection, if_exists="replace", index=False)
    orders.to_sql("fact_sales", connection, if_exists="replace", index=False)
    dates.to_sql("dim_date", connection, if_exists="replace", index=False)

print(f"Created {len(customers)} customers, {len(products)} products, and {len(orders)} orders.")
print(f"CSV files: {DATA_DIR}")
print(f"SQLite database: {DATABASE_DIR / 'retail_sales.db'}")
