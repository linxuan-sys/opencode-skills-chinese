---
name: docx
description: "当用户需要创建、读取、编辑或操作Word文档（.docx文件）时使用本技能。触发场景包括：任何提及'Word doc'、'word document'、'.docx'的内容，或生成带目录、标题、页码、信头格式的专业文档的需求。也适用于从.docx文件提取或重组内容、在文档中插入或替换图片、在Word文件中执行查找替换、处理修订或评论、或将内容转换为精美Word文档的场景。如果用户要求生成Word或.docx格式的'报告'、'备忘录'、'信件'、'模板'或类似交付物，使用本技能。请勿用于PDF、电子表格、Google Docs或与文档生成无关的通用编码任务。"
license: 专有。LICENSE.txt包含完整条款
---

# DOCX创建、编辑与分析

## 概述

.docx文件是包含XML文件的ZIP压缩包。

## 快速参考

| 任务 | 实现方式 |
| - | - |
| 读取/分析内容 | `pandoc` 或解包获取原始XML |
| 创建新文档 | 使用 `docx-js` - 参考下方创建新文档部分 |
| 编辑现有文档 | 解包 → 编辑XML → 重新打包 - 参考下方编辑现有文档部分 |

### 将.doc转换为.docx

旧版`.doc`文件必须先转换才能编辑：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 提取包含修订的文本
pandoc --track-changes=all document.docx -o output.md

# 访问原始XML
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图片

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受所有修订

生成已接受所有修订的干净文档（需要LibreOffice）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

使用JavaScript生成.docx文件，然后验证。安装依赖：`npm install -g docx`

### 初始化

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证

创建文件后进行验证。如果验证失败，解包、修复XML、重新打包。

```bash
python scripts/office/validate.py doc.docx
```

### 页面尺寸

```javascript
// 重要提示: docx-js默认使用A4，而非美国Letter尺寸
// 始终显式设置页面尺寸以获得一致结果
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5英寸，单位DXA
        height: 15840   // 11英寸，单位DXA
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1英寸边距
    }
  },
  children: [/* 内容 */]
}]
```

**常用页面尺寸（DXA单位，1440 DXA = 1英寸）：**

| 纸张类型 | 宽度 | 高度 | 内容宽度（1英寸边距） |
| ------- | ------- | -------- | ------------------------ |
| US Letter | 12,240 | 15,840 | 9,360 |
| A4（默认） | 11,906 | 16,838 | 9,026 |

**横向布局：** docx-js会内部交换宽度/高度，因此传入纵向尺寸让它自动处理交换：

```javascript
size: {
  width: 12240,   // 将短边作为width传入
  height: 15840,  // 将长边作为height传入
  orientation: PageOrientation.LANDSCAPE  // docx-js会在XML中交换它们
},
// 内容宽度 = 15840 - 左边距 - 右边距（使用长边）
```

### 样式（覆盖内置标题样式）

使用Arial作为默认字体（通用支持）。标题保持黑色以提高可读性。

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 默认12pt
    paragraphStyles: [
      // 重要提示: 使用精确的ID覆盖内置样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel是目录必需的
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题")] }),
    ]
  }]
});
```

### 列表（切勿使用Unicode项目符号）

```javascript
// ❌ 错误 - 切勿手动插入项目符号字符
new Paragraph({ children: [new TextRun("• 项目")] })  // 错误
new Paragraph({ children: [new TextRun("\u2022 项目")] })  // 错误

// ✅ 正确 - 使用带LevelFormat.BULLET的编号配置
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("项目符号项")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("编号项")] }),
    ]
  }]
});

// ⚠️ 每个reference创建独立的编号序列
// 相同reference = 编号连续 (1,2,3 接着 4,5,6)
// 不同reference = 编号重新开始 (1,2,3 接着 1,2,3)
```

### 表格

**重要提示：表格需要双重宽度设置** - 同时设置表格的`columnWidths`和每个单元格的`width`。缺少任意一个，表格在某些平台会渲染错误。

```javascript
// 重要提示: 始终设置表格宽度以保证渲染一致
// 重要提示: 使用ShadingType.CLEAR（而非SOLID）避免黑色背景
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 始终使用DXA（百分比在Google Docs中失效）
  columnWidths: [4680, 4680], // 总和必须等于表格宽度（DXA：1440 = 1英寸）
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 每个单元格也要设置
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR而非SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 单元格内边距（内部，不增加宽度）
          children: [new Paragraph({ children: [new TextRun("单元格")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算：**

始终使用`WidthType.DXA` — `WidthType.PERCENTAGE`在Google Docs中失效。

```javascript
// 表格宽度 = columnWidths之和 = 内容宽度
// 1英寸边距的US Letter: 12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // 总和必须等于表格宽度
```

**宽度规则：**

- **始终使用`WidthType.DXA`** — 切勿使用`WidthType.PERCENTAGE`（与Google Docs不兼容）
- 表格宽度必须等于`columnWidths`之和
- 单元格`width`必须与对应`columnWidth`匹配
- 单元格`margins`是内部内边距 - 会减少内容区域，不会增加单元格宽度
- 通栏表格：使用内容宽度（页面宽度减去左右边距）

### 图片

```javascript
// 重要提示: type参数是必需的
new Paragraph({
  children: [new ImageRun({
    type: "png", // 必需: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "标题", description: "描述", name: "名称" } // 三个属性都必需
  })]
})
```

### 分页符

```javascript
// 重要提示: PageBreak必须放在Paragraph内部
new Paragraph({ children: [new PageBreak()] })

// 或使用pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("新页面")] })
```

### 超链接

```javascript
// 外部链接
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "点击这里", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// 内部链接（书签 + 引用）
// 1. 在目标位置创建书签
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("第一章")] }),
]})
// 2. 链接到书签
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "查看第一章", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### 脚注

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("来源：2024年度报告")] },
    2: { children: [new Paragraph("方法学见附录")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("收入增长15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" 使用调整后指标"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### 制表位

```javascript
// 同一行右对齐文本（例如标题右侧的日期）
new Paragraph({
  children: [
    new TextRun("公司名称"),
    new TextRun("\t2025年1月"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// 点引导符（例如目录样式）
new Paragraph({
  children: [
    new TextRun("简介"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### 多列布局

```javascript
// 等宽列
sections: [{
  properties: {
    column: {
      count: 2,          // 列数
      space: 720,        // 列间距，单位DXA（720 = 0.5英寸）
      equalWidth: true,
      separate: true,    // 列之间显示竖线
    },
  },
  children: [/* 内容会自动跨列流动 */]
}]

// 自定义宽度列（equalWidth必须为false）
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* 内容 */]
}]
```

使用`type: SectionType.NEXT_COLUMN`的新节强制列分页。

### 目录

```javascript
// 重要提示: 标题必须仅使用HeadingLevel - 不能使用自定义样式
new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1英寸
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("页眉")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("第 "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" 页")]
    })] })
  },
  children: [/* 内容 */]
}]
```

### docx-js重要规则

- **显式设置页面尺寸** - docx-js默认使用A4；美国文档使用US Letter（12240 x 15840 DXA）
- **横向布局：传入纵向尺寸** - docx-js会内部交换宽度/高度；将短边作为`width`，长边作为`height`，并设置`orientation: PageOrientation.LANDSCAPE`
- **切勿使用`\n`** - 使用独立的Paragraph元素
- **切勿使用Unicode项目符号** - 使用带编号配置的`LevelFormat.BULLET`
- **PageBreak必须放在Paragraph内** - 单独使用会生成无效XML
- **ImageRun需要`type`参数** - 始终指定png/jpg等类型
- **始终使用DXA设置表格`width`** - 切勿使用`WidthType.PERCENTAGE`（在Google Docs中失效）
- **表格需要双重宽度设置** - `columnWidths`数组和单元格`width`，两者必须匹配
- **表格宽度 = columnWidths之和** - 使用DXA时确保数值完全相加
- **始终添加单元格边距** - 使用`margins: { top: 80, bottom: 80, left: 120, right: 120 }`获得可读的内边距
- **使用`ShadingType.CLEAR`** - 表格底纹切勿使用SOLID
- **切勿将表格用作分隔线/规则线** - 单元格有最小高度，会渲染为空框（包括页眉/页脚中的表格）；改为在Paragraph上使用`border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }`。两栏页脚使用制表位（参考制表位部分），而非表格
- **目录仅支持HeadingLevel** - 标题段落不能使用自定义样式
- **覆盖内置样式** - 使用精确ID："Heading1"、"Heading2"等
- **包含`outlineLevel`** - 目录必需（H1为0，H2为1，依此类推）

---

## 编辑现有文档

**按顺序执行全部3个步骤。**

### 步骤1：解包

```bash
python scripts/office/unpack.py document.docx unpacked/
```

提取XML、格式化打印、合并相邻文本块，并将智能引号转换为XML实体（`&#x201C;`等）以确保编辑后保留。使用`--merge-runs false`跳过文本块合并。

### 步骤2：编辑XML

编辑`unpacked/word/`中的文件。参考下方XML参考部分的模式。

**修订和评论默认使用"Claude"作为作者**，除非用户明确要求使用其他名称。

**直接使用Edit工具进行字符串替换。不要编写Python脚本。** 脚本会引入不必要的复杂度。Edit工具会显示确切的替换内容。

**重要提示：新内容使用智能引号。** 添加带引号或撇号的文本时，使用XML实体生成智能引号：

```xml
<!-- 使用这些实体实现专业排版 -->
<w:t>这里&#x2019;有一个引号：&#x201C;你好&#x201D;</w:t>
```

| 实体 | 字符 |
| -------- | ----------- |
| `&#x2018;` | ‘（左单引号） |
| `&#x2019;` | ’（右单引号/撇号） |
| `&#x201C;` | “（左双引号） |
| `&#x201D;` | ”（右双引号） |

**添加评论：** 使用`comment.py`处理多个XML文件的模板（文本必须是预转义的XML）：

```bash
python scripts/comment.py unpacked/ 0 "包含&amp;和&#x2019;的评论文本"
python scripts/comment.py unpacked/ 1 "回复文本" --parent 0  # 回复评论0
python scripts/comment.py unpacked/ 0 "文本" --author "自定义作者"  # 自定义作者名称
```

然后在document.xml中添加标记（参考XML参考中的评论部分）。

### 步骤3：打包

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

执行自动修复验证、压缩XML并生成DOCX。使用`--validate false`跳过验证。

**自动修复会处理：**

- `durableId` >= 0x7FFFFFFF（重新生成有效ID）
- 带空白的`<w:t>`缺少`xml:space="preserve"`的问题

**自动修复不会处理：**

- 格式错误的XML、无效元素嵌套、缺少关联、架构违规

### 常见陷阱

- **替换整个`<w:r>`元素**：添加修订时，将整个`<w:r>...</w:r>`块替换为同级的`<w:del>...<w:ins>...`。不要在文本块内部注入修订标签。
- **保留`<w:rPr>`格式**：将原始文本块的`<w:rPr>`块复制到修订文本块中，以保持粗体、字体大小等格式。

---

## XML参考

### 架构合规性

- **`<w:pPr>`中的元素顺序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`、最后是`<w:rPr>`
- **空白处理**：带前后空格的`<w:t>`添加`xml:space="preserve"`
- **RSIDs**：必须是8位十六进制（例如`00AB1234`）

### 修订

**插入：**

```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>插入的文本</w:t></w:r>
</w:ins>
```

**删除：**

```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
```

**`<w:del>`内部**：使用`<w:delText>`替代`<w:t>`，使用`<w:delInstrText>`替代`<w:instrText>`。

**最小化编辑** - 仅标记更改部分：

```xml
<!-- 将"30天"改为"60天" -->
<w:r><w:t>期限为 </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> 天。</w:t></w:r>
```

**删除整个段落/列表项** - 移除段落的所有内容时，也要将段落标记标记为已删除，使其与下一段落合并。在`<w:pPr><w:rPr>`中添加`<w:del/>`：

```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- 列表编号（如果存在） -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>正在删除的整个段落内容...</w:delText></w:r>
  </w:del>
</w:p>
```

如果`<w:pPr><w:rPr>`中缺少`<w:del/>`，接受修订后会留下空段落/列表项。

**拒绝其他作者的插入** - 将删除嵌套在他们的插入中：

```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>他们插入的文本</w:delText></w:r>
  </w:del>
</w:ins>
```

**恢复其他作者的删除** - 在后面添加插入（不要修改他们的删除）：

```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>删除的文本</w:t></w:r>
</w:ins>
```

### 评论

运行`comment.py`后（参考步骤2），在document.xml中添加标记。回复使用`--parent`参数并将标记嵌套在父标记内。

**重要提示：`<w:commentRangeStart>`和`<w:commentRangeEnd>`是`<w:r>`的同级元素，绝不能放在`<w:r>`内部。**

```xml
<!-- 评论标记是w:p的直接子元素，绝不能放在w:r内部 -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>删除的</w:delText></w:r>
</w:del>
<w:r><w:t> 更多文本</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- 评论0包含嵌套的回复1 -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>文本</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 图片生成

1. 将图片文件添加到`word/media/`
2. 在`word/_rels/document.xml.rels`中添加关联：

```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```

1. 在`[Content_Types].xml`中添加内容类型：

```xml
<Default Extension="png" ContentType="image/png"/>
```

1. 在document.xml中引用：

```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMU单位：914400 = 1英寸 -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

---

## 依赖

- **pandoc**：文本提取
- **docx**：`npm install -g docx`（新建文档）
- **LibreOffice**：PDF转换（通过`scripts/office/soffice.py`为沙箱环境自动配置）
- **Poppler**：`pdftoppm`用于图片转换
