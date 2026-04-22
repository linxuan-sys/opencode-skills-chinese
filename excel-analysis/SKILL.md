---
name: Excel Analysis
description: 分析Excel电子表格、创建数据透视表、生成图表和执行数据分析。在分析Excel文件、电子表格、表格数据或.xlsx文件时使用。
---

# Excel数据分析

## 快速开始

使用pandas读取Excel文件：

```python
import pandas as pd

# Read Excel file
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# Display first few rows
print(df.head())

# Basic statistics
print(df.describe())
```

## 读取多个工作表

处理工作簿中的所有工作表：

```python
import pandas as pd

# Read all sheets
excel_file = pd.ExcelFile("workbook.xlsx")

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"\n{sheet_name}:")
    print(df.head())
```

## 数据分析

执行常用分析任务：

```python
import pandas as pd

df = pd.read_excel("sales.xlsx")

# Group by and aggregate
sales_by_region = df.groupby("region")["sales"].sum()
print(sales_by_region)

# Filter data
high_sales = df[df["sales"] > 10000]

# Calculate metrics
df["profit_margin"] = (df["revenue"] - df["cost"]) / df["revenue"]

# Sort by column
df_sorted = df.sort_values("sales", ascending=False)
```

## 创建Excel文件

将数据写入Excel并设置格式：

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150],
    "Profit": [20, 40, 30]
})

# Write to Excel
writer = pd.ExcelWriter("output.xlsx", engine="openpyxl")
df.to_excel(writer, sheet_name="Sales", index=False)

# Get worksheet for formatting
worksheet = writer.sheets["Sales"]

# Auto-adjust column widths
for column in worksheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        if len(str(cell.value)) > max_length:
            max_length = len(str(cell.value))
    worksheet.column_dimensions[column_letter].width = max_length + 2

writer.close()
```

## 数据透视表

通过代码创建数据透视表：

```python
import pandas as pd

df = pd.read_excel("sales_data.xlsx")

# Create pivot table
pivot = pd.pivot_table(
    df,
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

print(pivot)

# Save pivot table
pivot.to_excel("pivot_report.xlsx")
```

## 图表与可视化

根据Excel数据生成图表：

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("data.xlsx")

# Create bar chart
df.plot(x="category", y="value", kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("chart.png")

# Create pie chart
df.set_index("category")["value"].plot(kind="pie", autopct="%1.1f%%")
plt.title("Market Share")
plt.ylabel("")
plt.savefig("pie_chart.png")
```

## 数据清洗

清洗和预处理Excel数据：

```python
import pandas as pd

df = pd.read_excel("messy_data.xlsx")

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.fillna(0)  # or df.dropna()

# Remove whitespace
df["name"] = df["name"].str.strip()

# Convert data types
df["date"] = pd.to_datetime(df["date"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Save cleaned data
df.to_excel("cleaned_data.xlsx", index=False)
```

## 合并与连接

合并多个Excel文件：

```python
import pandas as pd

# Read multiple files
df1 = pd.read_excel("sales_q1.xlsx")
df2 = pd.read_excel("sales_q2.xlsx")

# Concatenate vertically
combined = pd.concat([df1, df2], ignore_index=True)

# Merge on common column
customers = pd.read_excel("customers.xlsx")
sales = pd.read_excel("sales.xlsx")

merged = pd.merge(sales, customers, on="customer_id", how="left")

merged.to_excel("merged_data.xlsx", index=False)
```

## 高级格式设置

应用条件格式和样式：

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font

# Create Excel file
df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150]
})

df.to_excel("formatted.xlsx", index=False)

# Load workbook for formatting
wb = load_workbook("formatted.xlsx")
ws = wb.active

# Apply conditional formatting
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")

for row in range(2, len(df) + 2):
    cell = ws[f"B{row}"]
    if cell.value < 150:
        cell.fill = red_fill
    else:
        cell.fill = green_fill

# Bold headers
for cell in ws[1]:
    cell.font = Font(bold=True)

wb.save("formatted.xlsx")
```

## 性能优化建议

- 使用`read_excel`时搭配`usecols`参数仅读取指定列
- 处理超大文件时使用`chunksize`参数分块读取
- 根据文件类型选择使用`engine='openpyxl'`
- 使用`dtype`参数指定列类型以提升读取速度

## 可用依赖包

- **pandas** - 数据分析与处理（核心依赖）
- **openpyxl** - Excel文件创建与格式设置
- **xlsxwriter** - 高级Excel写入功能
- **matplotlib** - 图表生成
