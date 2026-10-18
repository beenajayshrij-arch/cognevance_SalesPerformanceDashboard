"""Step 2 - Analyse the data, create charts and write the report."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "screenshots"
df = pd.read_csv(ROOT / "data" / "cleaned_sales_data.csv", parse_dates=["Order Date"])
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
BLUE, GREEN, ORANGE = "#2563eb", "#16a34a", "#f59e0b"

# ---- KPIs ----
total_sales, total_profit = df["Sales"].sum(), df["Profit"].sum()
orders, margin = df["Order ID"].nunique(), total_profit / total_sales * 100
aov = total_sales / orders

monthly = df.groupby(["Month Number", "Month"])[["Sales", "Profit"]].sum().reset_index()
cat = df.groupby("Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
reg = df.groupby("Region")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
top_prod = df.groupby("Product Name")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False).head(10)
sub = df.groupby("Sub-Category")["Profit"].sum().sort_values()
seg = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)

# ---- Charts ----
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly["Month"], monthly["Sales"], marker="o", color=BLUE, label="Sales")
ax.plot(monthly["Month"], monthly["Profit"], marker="o", color=GREEN, label="Profit")
ax.set_title("Monthly Sales and Profit Trend (2025)"); ax.legend(); ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig(SHOTS / "01_monthly_trend_line.png", dpi=150); plt.close()

fig, ax = plt.subplots(figsize=(9, 4.5))
top_prod["Sales"].sort_values().plot.barh(ax=ax, color=BLUE)
ax.set_title("Top 10 Products by Sales"); ax.set_ylabel("")
fig.tight_layout(); fig.savefig(SHOTS / "02_top_products_bar.png", dpi=150); plt.close()

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(cat["Sales"], labels=cat.index, autopct="%1.1f%%", startangle=90,
       colors=[BLUE, GREEN, ORANGE], wedgeprops={"edgecolor": "white"})
ax.set_title("Sales Share by Category")
fig.tight_layout(); fig.savefig(SHOTS / "03_category_pie.png", dpi=150); plt.close()

fig, ax = plt.subplots(figsize=(8, 4.5))
x = range(len(reg))
ax.bar([i - .2 for i in x], reg["Sales"], .4, label="Sales", color=BLUE)
ax.bar([i + .2 for i in x], reg["Profit"], .4, label="Profit", color=GREEN)
ax.set_xticks(list(x)); ax.set_xticklabels(reg.index); ax.legend(); ax.set_title("Sales and Profit by Region")
fig.tight_layout(); fig.savefig(SHOTS / "04_region_bar.png", dpi=150); plt.close()

fig, ax = plt.subplots(figsize=(8, 4.5))
sub.plot.barh(ax=ax, color=[GREEN if v >= 0 else "#dc2626" for v in sub])
ax.set_title("Profit by Sub-Category"); ax.set_ylabel("")
fig.tight_layout(); fig.savefig(SHOTS / "05_subcategory_profit.png", dpi=150); plt.close()

# ---- Report ----
f = lambda v: f"{v:,.0f}"
best_m, worst_m = monthly.loc[monthly["Sales"].idxmax()], monthly.loc[monthly["Sales"].idxmin()]
q4 = df[df["Quarter"] == "Q4"]["Sales"].sum() / total_sales * 100
loss_sub = sub[sub < 0]
report = f"""# Sales Performance Analysis - Project Report

**Dataset:** Retail sales, Jan-Dec 2025 ({len(df):,} order lines, {orders:,} orders)
**Tools:** Python (pandas, matplotlib), interactive HTML dashboard, Power BI

## 1. Objective
Analyse monthly sales performance of a retail business, identify the best products,
categories and regions, and highlight where profit is being gained or lost.

## 2. Data Preparation
Duplicates removed, blanks filled (Sales recomputed from Unit Price x Quantity x (1 - Discount)),
text trimmed, Category casing standardised, dates converted and Month/Quarter columns added.
See `report/cleaning_log.txt`.

## 3. Key Metrics
| Metric | Value |
|---|---|
| Total Sales | {f(total_sales)} |
| Total Profit | {f(total_profit)} |
| Profit Margin | {margin:.1f}% |
| Total Orders | {orders:,} |
| Average Order Value | {f(aov)} |

## 4. Insights
1. **Top category:** {cat.index[0]} generates the most sales ({f(cat.iloc[0]['Sales'])}, {cat.iloc[0]['Sales']/total_sales*100:.1f}% of total).
2. **Most profitable category:** {cat['Profit'].idxmax()} ({f(cat['Profit'].max())} profit).
3. **Best region:** {reg.index[0]} leads with {f(reg.iloc[0]['Sales'])} in sales; {reg.index[-1]} is the weakest ({f(reg.iloc[-1]['Sales'])}).
4. **Top product:** {top_prod.index[0]} ({f(top_prod.iloc[0]['Sales'])} sales).
5. **Seasonality:** {best_m['Month']} was the best month ({f(best_m['Sales'])}) and {worst_m['Month']} the weakest ({f(worst_m['Sales'])}). Q4 contributes {q4:.1f}% of annual sales.
6. **Loss-making sub-categories:** {', '.join(loss_sub.index) if len(loss_sub) else 'None'}.
7. **Customer segments:** {seg.index[0]} is the largest segment ({seg.iloc[0]/seg.sum()*100:.1f}% of sales).

## 5. Recommendations
- Increase stock and marketing before Q4, the peak season.
- Review discounting on low-margin items, since higher discounts reduce profit.
- Monitor low-margin sub-categories and review their pricing and costs.
- Push campaigns in the weakest region ({reg.index[-1]}) to close the gap with {reg.index[0]}.
- Promote top-selling products with bundles and cross-selling.

## 6. Charts
![Monthly trend](../screenshots/01_monthly_trend_line.png)
![Top products](../screenshots/02_top_products_bar.png)
![Category share](../screenshots/03_category_pie.png)
![Region](../screenshots/04_region_bar.png)
![Sub-category profit](../screenshots/05_subcategory_profit.png)
"""
(ROOT / "report" / "Project_Report.md").write_text(report, encoding="utf-8")
print(f"Sales {f(total_sales)} | Profit {f(total_profit)} | Margin {margin:.1f}% | Orders {orders}")
print("Charts saved to screenshots/, report saved to report/Project_Report.md")
