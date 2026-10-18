# Build the same dashboard in Power BI Desktop

1. Open Power BI Desktop, then **Get Data > Text/CSV** and choose `data/cleaned_sales_data.csv`. Click **Load**.
2. In **Model view**, make sure `Order Date` is type Date and Sales/Profit are Decimal.
3. Add these measures (**Home > New measure**):

```DAX
Total Sales = SUM(cleaned_sales_data[Sales])
Total Profit = SUM(cleaned_sales_data[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales])
Total Orders = DISTINCTCOUNT(cleaned_sales_data[Order ID])
Avg Order Value = DIVIDE([Total Sales], [Total Orders])
```

4. Report page layout:
   - 4 **Card** visuals: Total Sales, Total Profit, Profit Margin %, Total Orders
   - **Line chart**: X = Month (sort by Month Number), Y = Total Sales, Total Profit
   - **Donut/Pie**: Legend = Category, Values = Total Sales
   - **Clustered bar**: Axis = Region, Values = Total Sales, Total Profit
   - **Bar chart**: Axis = Product Name, Values = Total Sales, then Filters pane > Top N = 10
5. Filters: add three **Slicer** visuals for `Category`, `Region` and `Month`.
6. Save as `dashboard/sales_dashboard.pbix`, then take screenshots into `screenshots/`.
