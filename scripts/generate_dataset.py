"""Generates a sample retail sales dataset (with a few realistic data-quality issues
so the cleaning step in Step 2 is meaningful)."""
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

catalog = {
    "Technology": {"Phones": (250, 900), "Laptops": (500, 1800), "Accessories": (10, 120)},
    "Furniture": {"Chairs": (60, 400), "Tables": (120, 700), "Storage": (30, 250)},
    "Office Supplies": {"Paper": (5, 40), "Binders": (3, 30), "Pens & Art": (2, 25)},
}
products = {
    "Phones": ["Galaxy Edge", "Pixel Pro", "iPhone Mini"],
    "Laptops": ["UltraBook 14", "WorkStation 15", "Student Lite"],
    "Accessories": ["Wireless Mouse", "USB-C Hub", "Bluetooth Speaker"],
    "Chairs": ["Ergo Chair", "Mesh Chair", "Executive Chair"],
    "Tables": ["Standing Desk", "Conference Table", "Study Table"],
    "Storage": ["Bookshelf", "File Cabinet", "Storage Rack"],
    "Paper": ["A4 Paper Ream", "Sticky Notes", "Notebook Pack"],
    "Binders": ["Ring Binder", "Clip Binder", "Document Folder"],
    "Pens & Art": ["Gel Pen Box", "Marker Set", "Highlighter Pack"],
}
regions = {
    "North": ["Delhi", "Jaipur"], "South": ["Chennai", "Bangalore"],
    "East": ["Kolkata", "Bhubaneswar"], "West": ["Mumbai", "Pune"],
}
segments = ["Consumer", "Corporate", "Small Business"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
margin_by_cat = {"Technology": (0.08, 0.28), "Furniture": (-0.05, 0.20), "Office Supplies": (0.15, 0.40)}

rows, start = [], date(2025, 1, 1)
for i in range(1, 2001):
    od = start + timedelta(days=random.randint(0, 364))
    # seasonality: more orders in Q4
    if od.month < 10 and random.random() < 0.15:
        od = date(2025, random.randint(10, 12), random.randint(1, 28))
    cat = random.choice(list(catalog))
    sub = random.choice(list(catalog[cat]))
    lo, hi = catalog[cat][sub]
    price = round(random.uniform(lo, hi), 2)
    qty = random.randint(1, 8)
    disc = random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20])
    sales = round(price * qty * (1 - disc), 2)
    m = random.uniform(*margin_by_cat[cat]) - disc * 0.5
    profit = round(sales * m, 2)
    region = random.choice(list(regions))
    rows.append({
        "Order ID": f"ORD-2025-{i:04d}",
        "Order Date": od.strftime("%d-%m-%Y"),
        "Ship Mode": random.choice(ship_modes),
        "Customer ID": f"CUST-{random.randint(1, 450):04d}",
        "Segment": random.choice(segments),
        "Region": region,
        "City": random.choice(regions[region]),
        "Category": cat,
        "Sub-Category": sub,
        "Product Name": random.choice(products[sub]),
        "Unit Price": price,
        "Quantity": qty,
        "Discount": disc,
        "Sales": sales,
        "Profit": profit,
    })

df = pd.DataFrame(rows)

# --- Inject realistic dirt for the cleaning step ---
for col, n in [("Region", 0), ("Segment", 12), ("Sales", 10), ("City", 15)]:
    if n:
        idx = df.sample(n, random_state=hash(col) % 1000).index
        df.loc[idx, col] = None
dups = df.sample(25, random_state=7)
df = pd.concat([df, dups], ignore_index=True).sample(frac=1, random_state=1).reset_index(drop=True)
idx = df.sample(20, random_state=3).index
df.loc[idx, "Category"] = df.loc[idx, "Category"].str.upper()          # inconsistent casing
idx = df.sample(20, random_state=4).index
df.loc[idx, "Product Name"] = " " + df.loc[idx, "Product Name"] + "  " # stray spaces

df.to_csv(str(__import__("pathlib").Path(__file__).resolve().parent.parent / "data" / "raw_sales_data.csv"), index=False)
print(df.shape)
