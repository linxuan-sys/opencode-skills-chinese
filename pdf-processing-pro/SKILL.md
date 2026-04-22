---
name: PDF处理专业版
description: 生产级PDF处理工具，支持表单、表格、OCR、验证和批量操作。适用于生产环境中的复杂PDF工作流、处理大量PDF或需要健壮的错误处理和验证时使用。
---

# PDF处理专业版

生产级PDF处理工具包，包含预构建脚本、全面的错误处理，支持复杂工作流。

## 快速开始

### 从PDF提取文本

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    print(text)
```

### 分析PDF表单（使用内置脚本）

```bash
python scripts/analyze_form.py input.pdf --output fields.json
# 返回包含所有表单字段、类型和位置的JSON
```

### 带验证填充PDF表单

```bash
python scripts/fill_form.py input.pdf data.json output.pdf
# 填充前验证所有字段，包含错误报告
```

### 从PDF提取表格

```bash
python scripts/extract_tables.py report.pdf --output tables.csv
# 自动检测列并提取所有表格
```

## 功能特性

### ✅ 生产级脚本

所有脚本都包含：
- **错误处理**：优雅失败并提供详细错误信息
- **验证机制**：输入验证和类型检查
- **日志功能**：带时间戳的可配置日志
- **类型提示**：完整类型注解，支持IDE智能补全
- **CLI接口**：所有脚本支持`--help`帮助命令
- **退出码**：标准退出码，适合自动化调用

### ✅ 全面工作流支持

- **PDF表单**：完整的表单处理流程
- **表格提取**：高级表格检测和提取功能
- **OCR处理**：扫描版PDF文本提取
- **批量操作**：高效处理多个PDF文件
- **验证机制**：预处理和后处理验证

## 高级主题

### PDF表单处理

完整的表单工作流支持：
- 字段分析和自动检测
- 动态表单填充
- 自定义验证规则
- 多页表单支持
- 复选框和单选按钮处理

详情参见[FORMS.md](FORMS.md)

### 表格提取

复杂表格提取支持：
- 跨页表格处理
- 合并单元格识别
- 嵌套表格支持
- 自定义表格检测
- 导出为CSV/Excel格式

详情参见[TABLES.md](TABLES.md)

### OCR处理

适用于扫描版PDF和图像文档：
- Tesseract OCR引擎集成
- 多语言支持
- 图像预处理优化
- 识别置信度评分
- 批量OCR处理

详情参见[OCR.md](OCR.md)

## 内置脚本说明

### 表单处理脚本

**analyze_form.py** - 提取表单字段信息
```bash
python scripts/analyze_form.py input.pdf [--output fields.json] [--verbose]
```

**fill_form.py** - 用数据填充PDF表单
```bash
python scripts/fill_form.py input.pdf data.json output.pdf [--validate]
```

**validate_form.py** - 填充前验证表单数据
```bash
python scripts/validate_form.py data.json schema.json
```

### 表格提取脚本

**extract_tables.py** - 提取表格到CSV/Excel
```bash
python scripts/extract_tables.py input.pdf [--output tables.csv] [--format csv|excel]
```

### 文本提取脚本

**extract_text.py** - 保留格式提取文本
```bash
python scripts/extract_text.py input.pdf [--output text.txt] [--preserve-formatting]
```

### 工具脚本

**merge_pdfs.py** - 合并多个PDF文件
```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf file3.pdf --output merged.pdf
```

**split_pdf.py** - 将PDF拆分为单独页面
```bash
python scripts/split_pdf.py input.pdf --output-dir pages/
```

**validate_pdf.py** - 验证PDF文件完整性
```bash
python scripts/validate_pdf.py input.pdf
```

## 常用工作流示例

### 工作流1：表单提交处理

```bash
# 1. 分析表单结构
python scripts/analyze_form.py template.pdf --output schema.json

# 2. 验证提交数据
python scripts/validate_form.py submission.json schema.json

# 3. 填充表单
python scripts/fill_form.py template.pdf submission.json completed.pdf

# 4. 验证输出文件
python scripts/validate_pdf.py completed.pdf
```

### 工作流2：报告数据提取

```bash
# 1. 提取表格数据
python scripts/extract_tables.py monthly_report.pdf --output data.csv

# 2. 提取文本用于分析
python scripts/extract_text.py monthly_report.pdf --output report.txt
```

### 工作流3：批量处理PDF

```python
import glob
from pathlib import Path
import subprocess

# 处理目录中所有PDF文件
for pdf_file in glob.glob("invoices/*.pdf"):
    output_file = Path("processed") / Path(pdf_file).name

    result = subprocess.run([
        "python", "scripts/extract_text.py",
        pdf_file,
        "--output", str(output_file)
    ], capture_output=True)

    if result.returncode == 0:
        print(f"✓ 处理完成：{pdf_file}")
    else:
        print(f"✗ 处理失败：{pdf_file} - {result.stderr}")
```

## 错误处理说明

所有脚本遵循一致的错误模式：

```python
# 退出码说明
# 0 - 处理成功
# 1 - 文件未找到
# 2 - 输入参数无效
# 3 - 处理过程出错
# 4 - 验证失败

# 自动化调用示例
result = subprocess.run(["python", "scripts/fill_form.py", ...])

if result.returncode == 0:
    print("处理成功")
elif result.returncode == 4:
    print("验证失败 - 请检查输入数据")
else:
    print(f"发生错误：错误码 {result.returncode}")
```

## 依赖安装

所有脚本需要安装以下依赖：

```bash
pip install pdfplumber pypdf pillow pytesseract pandas
```

OCR功能可选依赖：
```bash
# 安装tesseract-ocr系统包
# macOS：brew install tesseract
# Ubuntu：apt-get install tesseract-ocr
# Windows：从GitHub发布页面下载安装
```

## 性能优化建议

- **批量处理**多个PDF文件时使用批量模式
- **多进程支持**使用`--parallel`标志启用多进程（支持的脚本）
- **数据缓存**缓存已提取的数据，避免重复处理
- **提前验证**尽早验证输入，快速失败减少资源浪费
- **流式处理**处理大型PDF（>50MB）时使用流式处理

## 最佳实践

1. 处理前**始终验证输入**文件有效性
2. 自定义脚本中使用**try-except捕获异常**
3. **记录所有操作日志**，便于调试和排查问题
4. 生产环境部署前**使用样例PDF测试**
5. 为长时间运行的操作**设置超时时间**
6. 自动化调用中**检查返回码**判断执行结果
7. 修改文件前**备份原始文件**

## 常见问题排查

### 常见问题

**"模块未找到"错误：**
```bash
pip install -r requirements.txt
```

**未找到Tesseract程序：**
```bash
# 请先安装tesseract系统包（参考依赖安装说明）
```

**大型PDF处理内存不足：**
```python
# 逐页处理而非加载整个PDF文件
with pdfplumber.open("large.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # 立即处理当前页面，避免内存累积
```

**权限不足错误：**
```bash
chmod +x scripts/*.py
```

## 获取帮助

所有脚本都支持`--help`命令查看帮助：

```bash
python scripts/analyze_form.py --help
python scripts/extract_tables.py --help
```

特定主题的详细文档请参考：
- [FORMS.md](FORMS.md) - 完整表单处理指南
- [TABLES.md](TABLES.md) - 高级表格提取说明
- [OCR.md](OCR.md) - 扫描版PDF处理指南
