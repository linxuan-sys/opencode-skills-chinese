---
name: xlsx
description: "当电子表格文件是主要输入或输出时使用此技能。适用于用户需要执行以下操作的任何任务：打开、读取、编辑或修复现有.xlsx、.xlsm、.csv或.tsv文件（例如添加列、计算公式、格式化、制作图表、清理杂乱数据）；从零开始或从其他数据源创建新电子表格；或在表格类文件格式之间转换。尤其当用户通过名称或路径引用电子表格文件时——即使是随意提及（比如"我下载文件夹里的xlsx"）——并且需要对其进行操作或基于其生成内容时触发。也适用于清理或重构杂乱的表格数据文件（格式错误的行、错位的表头、垃圾数据）为规范的电子表格。交付物必须是电子表格文件。当主要交付物是Word文档、HTML报告、独立Python脚本、数据库流水线或Google Sheets API集成时，即使涉及表格数据也不要触发此技能。"
license: 专有。完整条款见LICENSE.txt
---

# 输出要求

## 所有Excel文件

### 专业字体
- 所有交付物使用统一的专业字体（例如Arial、Times New Roman），除非用户另有指示

### 零公式错误
- 交付的所有Excel模型必须零公式错误（#REF!、#DIV/0!、#VALUE!、#N/A、#NAME?）

### 保留现有模板（更新模板时）
- 修改文件时研究并严格匹配现有格式、样式和规范
- 不要对已有固定格式的文件强制使用标准化格式
- 现有模板规范始终优先于这些指南

## 财务模型

### 颜色编码标准
除非用户或现有模板另有说明

#### 行业标准颜色约定
- **蓝色文本（RGB: 0,0,255）**：硬编码输入值，以及用户会根据场景修改的数字
- **黑色文本（RGB: 0,0,0）**：所有公式和计算结果
- **绿色文本（RGB: 0,128,0）**：引用同一工作簿内其他工作表的链接
- **红色文本（RGB: 255,0,0）**：指向其他文件的外部链接
- **黄色背景（RGB: 255,255,0）**：需要关注的关键假设或需要更新的单元格

### 数字格式标准

#### 强制格式规则
- **年份**：格式化为文本字符串（例如"2024"而不是"2,024"）
- **货币**：使用$#,##0格式；始终在表头中指定单位（"收入 ($百万)"）
- **零值**：使用数字格式将所有零显示为"-"，包括百分比（例如"$#,##0;($#,##0);-"）
- **百分比**：默认使用0.0%格式（一位小数）
- **倍数**：估值倍数（EV/EBITDA、P/E）格式化为0.0x
- **负数**：使用括号表示(123)而不是减号-123

### 公式构建规则

#### 假设值放置位置
- 将所有假设值（增长率、利润率、倍数等）放在独立的假设单元格中
- 公式中使用单元格引用而不是硬编码值
- 示例：使用=B5*(1+$B$6)而不是=B5*1.05

#### 公式错误预防
- 验证所有单元格引用正确
- 检查范围是否存在差一错误
- 确保所有预测期的公式一致
- 使用边界情况测试（零值、负数）
- 确认没有意外的循环引用

#### 硬编码值的文档要求
- 添加注释或写在旁边的单元格中（如果是表格末尾）。格式："来源: [系统/文档], [日期], [具体引用], [URL（如果有）]"
- 示例：
  - "来源: 公司10-K报告, 2024财年, 第45页, 收入附注, [SEC EDGAR URL]"
  - "来源: 公司10-Q报告, 2025年第二季度, 附件99.1, [SEC EDGAR URL]"
  - "来源: Bloomberg Terminal, 2025年8月15日, AAPL US Equity"
  - "来源: FactSet, 2025年8月20日, 市场一致预期屏幕"

# XLSX创建、编辑和分析

## 概述

用户可能要求你创建、编辑或分析.xlsx文件的内容。针对不同任务可以使用不同的工具和工作流。

## 重要要求

**公式重新计算需要LibreOffice**：你可以假设已安装LibreOffice，使用`scripts/recalc.py`脚本重新计算公式值。脚本首次运行时会自动配置LibreOffice，包括Unix套接字受限的沙箱环境（由`scripts/office/soffice.py`处理）

## 读取和分析数据

### 使用pandas进行数据分析
对于数据分析、可视化和基础操作，使用**pandas**，它提供强大的数据处理能力：

```python
import pandas as pd

# 读取Excel
df = pd.read_excel('file.xlsx')  # 默认：第一个工作表
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # 所有工作表以字典形式返回

# 分析
df.head()      # 预览数据
df.info()      # 列信息
df.describe()  # 统计信息

# 写入Excel
df.to_excel('output.xlsx', index=False)
```

## Excel文件工作流

## 关键要求：使用公式，不要硬编码值

**始终使用Excel公式，而不是在Python中计算值然后硬编码**。这样可以确保电子表格保持动态可更新。

### ❌ 错误 - 硬编码计算结果
```python
# 错误：在Python中计算并硬编码结果
total = df['Sales'].sum()
sheet['B10'] = total  # 硬编码为5000

# 错误：在Python中计算增长率
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # 硬编码为0.15

# 错误：在Python中计算平均值
avg = sum(values) / len(values)
sheet['D20'] = avg  # 硬编码为42.5
```

### ✅ 正确 - 使用Excel公式
```python
# 正确：让Excel计算总和
sheet['B10'] = '=SUM(B2:B9)'

# 正确：增长率使用Excel公式
sheet['C5'] = '=(C4-C2)/C2'

# 正确：使用Excel函数计算平均值
sheet['D20'] = '=AVERAGE(D2:D19)'
```

这适用于所有计算——总计、百分比、比率、差值等。电子表格应该能够在源数据变化时重新计算。

## 通用工作流
1. **选择工具**：数据处理用pandas，公式/格式处理用openpyxl
2. **创建/加载**：创建新工作簿或加载现有文件
3. **修改**：添加/编辑数据、公式和格式
4. **保存**：写入文件
5. **重新计算公式（使用公式时必须执行）**：使用scripts/recalc.py脚本
   ```bash
   python scripts/recalc.py output.xlsx
   ```
6. **验证并修复所有错误**：
   - 脚本返回包含错误详情的JSON
   - 如果`status`为`errors_found`，查看`error_summary`获取具体错误类型和位置
   - 修复发现的错误后再次重新计算
   - 需要修复的常见错误：
     - `#REF!`：无效的单元格引用
     - `#DIV/0!`：除零错误
     - `#VALUE!`：公式中数据类型错误
     - `#NAME?`：无法识别的公式名称

### 创建新Excel文件

```python
# 使用openpyxl处理公式和格式
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# 添加数据
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# 添加公式
sheet['B2'] = '=SUM(A1:A10)'

# 格式化
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# 列宽
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有Excel文件

```python
# 使用openpyxl保留公式和格式
from openpyxl import load_workbook

# 加载现有文件
wb = load_workbook('existing.xlsx')
sheet = wb.active  # 或用wb['SheetName']指定工作表

# 处理多个工作表
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"工作表: {sheet_name}")

# 修改单元格
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # 在第2行位置插入行
sheet.delete_cols(3)  # 删除第3列

# 添加新工作表
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重新计算公式

openpyxl创建或修改的Excel文件包含字符串形式的公式，但没有计算值。使用提供的`scripts/recalc.py`脚本重新计算公式：

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

示例：
```bash
python scripts/recalc.py output.xlsx 30
```

脚本功能：
- 首次运行时自动设置LibreOffice宏
- 重新计算所有工作表中的所有公式
- 扫描所有单元格查找Excel错误（#REF!、#DIV/0!等）
- 返回包含详细错误位置和计数的JSON
- 同时支持Linux和macOS

## 公式验证检查清单

快速检查确保公式正常工作：

### 基本验证
- [ ] **测试2-3个示例引用**：在构建完整模型前验证它们获取的值正确
- [ ] **列映射**：确认Excel列匹配（例如第64列是BL，不是BK）
- [ ] **行偏移**：记住Excel行是1索引的（DataFrame第5行 = Excel第6行）

### 常见陷阱
- [ ] **NaN处理**：使用`pd.notna()`检查空值
- [ ] **最右侧列**：财年数据通常在第50列之后
- [ ] **多个匹配项**：搜索所有出现的位置，不只是第一个
- [ ] **除零错误**：在公式中使用`/`前检查分母（#DIV/0!）
- [ ] **引用错误**：验证所有单元格引用指向目标单元格（#REF!）
- [ ] **跨工作表引用**：链接工作表时使用正确格式（Sheet1!A1）

### 公式测试策略
- [ ] **从小范围开始**：先在2-3个单元格上测试公式，再广泛应用
- [ ] **验证依赖项**：检查公式中引用的所有单元格都存在
- [ ] **测试边界情况**：包括零、负数和非常大的值

### 解读scripts/recalc.py输出
脚本返回包含错误详情的JSON：
```json
{
  "status": "success",           // 或"errors_found"
  "total_errors": 0,              // 总错误数
  "total_formulas": 42,           // 文件中的公式数量
  "error_summary": {              // 仅当发现错误时存在
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳实践

### 库选择
- **pandas**：最适合数据分析、批量操作和简单数据导出
- **openpyxl**：最适合复杂格式、公式和Excel特有功能

### 使用openpyxl
- 单元格索引是1索引的（row=1, column=1对应单元格A1）
- 使用`data_only=True`读取计算后的值：`load_workbook('file.xlsx', data_only=True)`
- **警告**：如果以`data_only=True`打开并保存，公式会被替换为值并永久丢失
- 大文件处理：读取时使用`read_only=True`，写入时使用`write_only=True`
- 公式会被保留但不会计算——使用scripts/recalc.py更新值

### 使用pandas
- 指定数据类型避免推断错误：`pd.read_excel('file.xlsx', dtype={'id': str})`
- 大文件读取指定列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 正确处理日期：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 代码风格指南
**重要**：生成Excel操作的Python代码时：
- 编写简洁的Python代码，不要不必要的注释
- 避免冗长的变量名和冗余操作
- 避免不必要的print语句

**对于Excel文件本身**：
- 给包含复杂公式或重要假设的单元格添加注释
- 记录硬编码值的数据来源
- 为关键计算和模型部分添加说明