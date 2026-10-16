---
name: chart-generator
description: 按照用户自定义的matplotlib规范和antv MCP工具生成各类可视化图表。使用当用户提到生成图表、柱状图、折线图、饼图、散点图、雷达图、可视化数据时触发。
scope: global
license: MIT
---


# 图表生成Skill

## 适用场景

用户需要生成数据可视化图表时自动触发，支持两种生成方式：

1. 轻量快速图表：调用antv MCP工具直接生成
2. 定制化PNG图表：严格按照用户指定的matplotlib规范生成，输出到Downloads目录

## 执行流程

### Step 1: 确认需求

自动收集必要参数，缺失时询问用户：

- 图表类型（柱状图/折线图/饼图/散点图/雷达图/面积图等）
- 具体数据（包含维度和数值）
- 可选参数：标题、x轴标签、y轴标签、是否堆叠、颜色主题等

### Step 2: 选择生成方式

- 优先用antv MCP工具：适合快速生成、不需要本地文件的场景
- 自动切换matplotlib：用户要求导出PNG、需要定制化样式、antv不支持的图表类型时使用

### Step 3: 按规范生成

#### Matplotlib生成规范（严格执行用户配置）

1. 必须使用Agg后端，无GUI模式
2. 全局字体设置：

   ```python
   plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
   plt.rcParams['axes.unicode_minus'] = False
   ```

3. 输出路径固定为`/home/LinXuan/Downloads/图表名.png`，dpi=150
4. 自动添加紧凑布局：`plt.tight_layout()`

#### Antv MCP生成规范

1. 优先选择对应类型的antv工具调用
2. 自动补全用户未指定的默认参数（宽高默认600x400，主题默认default）
3. 生成后直接返回结果给用户

### Step 4: 结果反馈

- Matplotlib生成：告知用户文件保存路径，确认生成成功
- Antv生成：直接展示生成的图表结果

## 触发关键词

生成图表、画个图、柱状图、折线图、饼图、散点图、雷达图、面积图、数据可视化、matplotlib画图、antv图表

## 禁止场景

- 非图表生成类请求
- 要求生成Excel/Word等非可视化格式的请求
