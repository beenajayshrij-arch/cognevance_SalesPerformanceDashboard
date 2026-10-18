"""Step 1 - Clean the raw sales data."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "raw_sales_data.csv")
log = [f"Raw rows: {len(df)}"]

# 1. Remove duplicate rows
n = df.duplicated().sum()
df = df.drop_duplicates()
log.append(f"Duplicate rows removed: {n}")

# 2. Trim stray spaces and fix inconsistent casing
for col in ["Product Name", "Category", "Sub-Category", "City", "Segment", "Region"]:
    df[col] = df[col].astype("string").str.strip()
df["Category"] = df["Category"].str.title()
log.append("Trimmed spaces and standardised Category casing")

# 3. Handle missing values
miss = df.isna().sum()
log.append(f"Missing before: {miss[miss > 0].to_dict()}")
calc = (df["Unit Price"] * df["Quantity"] * (1 - df["Discount"])).round(2)
df["Sales"] = df["Sales"].fillna(calc)           # recompute missing Sales
df["Segment"] = df["Segment"].fillna("Unknown")
df["City"] = df["City"].fillna("Unknown")

# 4. Fix data types and add date features
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
df["Year"] = df["Order Date"].dt.year
df["Month Number"] = df["Order Date"].dt.month
df["Month"] = df["Order Date"].dt.strftime("%b")
df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
df = df.sort_values("Order Date").reset_index(drop=True)

log.append(f"Missing after: {int(df.isna().sum().sum())}")
log.append(f"Clean rows: {len(df)}")
df.to_csv(ROOT / "data" / "cleaned_sales_data.csv", index=False)
(ROOT / "report" / "cleaning_log.txt").write_text("\n".join(log), encoding="utf-8")
print("\n".join(log))
