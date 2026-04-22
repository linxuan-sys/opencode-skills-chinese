---
name: ppt-generation
description: 当用户要求生成、创建或制作演示文稿（PPT/PPTX）时使用此技能。通过为每一页幻灯片生成配图并组合成PowerPoint文件，创建视觉效果丰富的演示文稿。
---

# PPT生成技能

## 概述

本技能通过为每一页幻灯片生成AI配图，然后组合成完整的PPTX文件，实现专业级演示文稿生成。工作流包括：规划统一视觉风格的演示文稿结构、按顺序生成每一页幻灯片图像（以上一页为参考保证风格统一）、最终合成完整的演示文稿文件。

## 核心功能

* 规划多页演示文稿结构，保证整体视觉风格统一
* 支持8种演示风格：商务风、学术风、极简风、苹果Keynote风、创意风等
* 调用图像生成技能为每一页生成专属AI配图
* 使用相同的seed和风格提示词，保证整体视觉一致性
* 合成专业级PPTX文件

## 演示风格

创建演示文稿计划时，请从以下风格中选择：

| 风格 | 描述 | 最佳适用场景 |
|-------|-------------|----------|
| **玻璃态风格** | 毛玻璃面板加模糊效果、浮动半透明卡片、活力渐变背景、分层深度感 | 科技产品、AI/SaaS演示、未来感发布会 |
| **暗黑高端风** | 深黑色背景(#0a0a0a)、亮色调强调色、微妙发光效果、奢侈品牌质感 | 高端产品、高管汇报、奢侈品品牌 |
| **渐变现代风** | 大胆的网格渐变、流畅色彩过渡、现代排版、活力且专业 | 创业公司、创意机构、品牌发布会 |
| **新粗野主义风** | 粗犷的加粗字体、高对比度、刻意的「粗糙」美学、反传统设计、孟菲斯风格灵感 | 潮流品牌、面向Z世代的内容、颠覆性创业项目 |
| **3D等距风格** | 简洁的等距3D插图、浮动3D元素、柔和阴影、科技感美学 | 科技原理讲解、产品功能介绍、SaaS演示 |
| **杂志编辑风** | 杂志级排版、精致的字体层级、戏剧化摄影、Vogue/彭博商业周刊质感 | 年度报告、奢侈品品牌、思想领导力内容 |
| **极简瑞士风** | 严格网格排版、Helvetica风格字体、大量留白、永恒现代感 | 建筑设计、设计公司、高端咨询 |
| **Keynote风格** | 苹果风格美学、粗体字体、戏剧化图像、高对比度、影院级质感 | 主题演讲、产品发布会、励志分享 |

## 工作流

### 步骤1：理解需求

用户要求生成演示文稿时，确认以下信息：

* 主题：演示文稿的核心内容
* 页数：需要多少页（默认5-10页）
* **风格**：商务/学术/极简/Keynote/创意风等
* 宽高比：标准(16:9)或经典(4:3)
* 内容大纲：每页的核心要点
* 无需检查`/home/LinXuan/Downloads`目录

### 步骤2：创建演示文稿计划

在`/home/LinXuan/Downloads/`下创建JSON格式的演示结构文件。**重要：** 必须包含`style`字段以定义整体视觉一致性。

```json
{
  "title": "演示文稿标题",
  "style": "keynote",
  "style_guidelines": {
    "color_palette": "深黑色背景、白色文字、单一强调色（蓝色或橙色）",
    "typography": "粗体无衬线标题、清晰正文、显著的字号对比",
    "imagery": "高质量摄影、全出血图像、影院级构图",
    "layout": "充足留白、内容居中、每页元素极简"
  },
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "主标题",
      "subtitle": "副标题或宣传语",
      "visual_description": "图像生成的详细描述"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "幻灯片标题",
      "key_points": ["要点1", "要点2", "要点3"],
      "visual_description": "图像生成的详细描述"
    }
  ]
}
```

### 步骤3：按顺序生成幻灯片图像

**重要提示：** 必须**严格按顺序逐页生成**，禁止并行或批量生成图像。每一页都依赖完全一致的风格提示词和固定的seed保证风格一致性，并行生成会破坏视觉一致性，严格禁止。

1. 调用 `tongyi_wanx-t2i-image-generation` MCP工具生成图像，通过 `tongyi_wanx-t2i-image-generation-result` 获取结果URL，并用 curl 下载到 /home/LinXuan/Downloads/ 目录。

2. **第一页幻灯片（第1页）**：创建提示词，确立整体视觉语言：

```json
{
  "prompt": "专业演示文稿标题页。[计划中的风格指南]。标题：'你的标题'。[视觉描述]。此页将确立整个演示文稿的视觉语言。",
  "style": "[基于所选风格 - 例如：苹果Keynote美学、戏剧化光线、影院级质感]",
  "composition": "清晰的文本层级、简洁排版、[对应风格的布局]",
  "color_palette": "[来自风格指南]",
  "typography": "[来自风格指南]"
}
```

```bash
# 1. 使用 tongyi_wanx-t2i-image-generation 工具提交生图任务，设置 prompt, negative_prompt 和相同的 seed (如 12345)
# 2. 使用 tongyi_wanx-t2i-image-generation-result 工具轮询获取图片 URL
# 3. 下载图片到本地的 Downloads 目录
curl -s -o /home/LinXuan/Downloads/slide-0X.jpg "获取到的URL"
```

1. **后续页面（第2页及以后）**：使用**上一页**作为参考图：

```json
{
  "prompt": "演示文稿页面，严格延续参考图像的视觉风格。保持相同的调色板、字体风格和整体美学。标题：'幻灯片标题'。[视觉描述]。与参考图保持视觉一致性。",
  "style": "完全匹配参考图 - 玻璃态风格、visionOS美学、相同视觉语言",
  "composition": "与参考图相似的布局原则，适配当前内容",
  "color_palette": "完全匹配参考图",
  "consistency_note": "此页面必须看起来与参考图属于同一演示文稿"
}
```

```bash
# 1. 使用 tongyi_wanx-t2i-image-generation 工具提交生图任务，设置 prompt, negative_prompt 和相同的 seed (如 12345)
# 2. 使用 tongyi_wanx-t2i-image-generation-result 工具轮询获取图片 URL
# 3. 下载图片到本地的 Downloads 目录
curl -s -o /home/LinXuan/Downloads/slide-0X.jpg "获取到的URL"
```

1. **剩余页面继续按此逻辑生成**，始终保持一致的提示词和seed：

```bash
# 第3页引用第2页
# 1. 使用 tongyi_wanx-t2i-image-generation 工具提交生图任务，设置 prompt, negative_prompt 和相同的 seed (如 12345)
# 2. 使用 tongyi_wanx-t2i-image-generation-result 工具轮询获取图片 URL
# 3. 下载图片到本地的 Downloads 目录
curl -s -o /home/LinXuan/Downloads/slide-0X.jpg "获取到的URL"

# 第4页引用第3页
# 1. 使用 tongyi_wanx-t2i-image-generation 工具提交生图任务，设置 prompt, negative_prompt 和相同的 seed (如 12345)
# 2. 使用 tongyi_wanx-t2i-image-generation-result 工具轮询获取图片 URL
# 3. 下载图片到本地的 Downloads 目录
curl -s -o /home/LinXuan/Downloads/slide-0X.jpg "获取到的URL"
```

### 步骤4：合成PPT文件

所有幻灯片图像生成完成后，调用合成脚本：

```bash
python /home/LinXuan/.config/opencode/skills/ppt-generation/scripts/generate.py \
  --plan-file /home/LinXuan/Downloads/presentation-plan.json \
  --slide-images /home/LinXuan/Downloads/slide-01.jpg /home/LinXuan/Downloads/slide-02.jpg /home/LinXuan/Downloads/slide-03.jpg \
  --output-file /home/LinXuan/Downloads/presentation.pptx
```

参数说明：

* `--plan-file`：演示文稿计划JSON文件的绝对路径（必填）
* `--slide-images`：按顺序排列的幻灯片图像绝对路径（必填，空格分隔）
* `--output-file`：输出PPTX文件的绝对路径（必填）

> 注意：无需读取Python文件内容，直接按参数调用即可。

## 完整示例：玻璃态风格（最现代前卫）

用户需求：「创建一个关于AI产品发布的演示文稿」

### 步骤1：创建演示文稿计划

创建`/home/LinXuan/Downloads/ai-product-plan.json`：

```json
{
  "title": "Nova AI 隆重登场",
  "style": "glassmorphism",
  "style_guidelines": {
    "color_palette": "活力渐变背景（紫色#667eea到青色#00d4ff）、20%透明度的磨砂白色面板、醒目的强调色",
    "typography": "SF Pro Display风格、600-700粗体标题、400字重清晰正文、白色文字加微妙阴影保证在玻璃上的可读性",
    "imagery": "悬浮的抽象3D形状、柔和模糊球体、玻璃材质的几何基础图形、通过重叠半透明层营造深度感",
    "layout": "带背景模糊效果的浮动卡片面板、充足内边距(48-64px)、圆角(24-32px半径)、通过微妙阴影营造分层深度",
    "effects": "毛玻璃模糊（backdrop-filter: blur 20px）、微妙白色边框(1px rgba 255,255,255,0.2)、面板后柔光效果、带阴影的浮动元素",
    "visual_language": "苹果Vision Pro/visionOS UI美学、通过透明度营造深度感、光线穿过玻璃表面的折射效果"
  },
  "aspect_ratio": "16:9",
  "slides": [
    {
      "slide_number": 1,
      "type": "title",
      "title": "Nova AI 隆重登场",
      "subtitle": "智能，全新定义",
      "visual_description": "惊艳的渐变背景，从深紫色(#667eea)过渡到洋红色再到青色(#00d4ff)。中央：大型磨砂玻璃面板带强背景模糊效果，包含粗体白色标题'Nova AI 隆重登场'和更浅色的副标题。卡片周围悬浮3D玻璃球体和抽象形状营造深度感。玻璃面板后方透出柔和光晕。高级visionOS美学。玻璃面板带有微妙的白色边框(1px rgba 255,255,255,0.3)和淡紫色调阴影。"
    },
    {
      "slide_number": 2,
      "type": "content",
      "title": "为什么选择Nova？",
      "key_points": ["10倍更快处理速度", "类人理解能力", "企业级安全保障"],
      "visual_description": "相同的紫青渐变背景。左侧：浮动磨砂玻璃卡片，包含粗体白色标题'为什么选择Nova？'，下方是三个要点，配微妙玻璃药丸徽章。右侧：神经网络的抽象3D可视化，由带柔和青色发光的互联玻璃节点构成，悬浮在空间中。浮动的半透明几何形状（二十面体、圆环）与参考风格一致，增加深度感。保持与上一页完全相同的玻璃态美学。"
    },
    {
      "slide_number": 3,
      "type": "content",
      "title": "工作原理",
      "key_points": ["自然语言输入", "多模态处理", "即时洞察输出"],
      "visual_description": "渐变背景与前几页一致。中央布局：三层略微倾斜的磨砂玻璃卡片展示工作流步骤，由柔和发光线条连接。每张卡片带有抽象图标。周围浮动玻璃球体和光粒子。顶部是粗体白色标题'工作原理'。通过卡片层叠和透明度营造深度感。"
    },
    {
      "slide_number": 4,
      "type": "content",
      "title": "为大规模场景打造",
      "key_points": ["支持百万级并发用户", "99.99%可用性", "全球基础设施"],
      "visual_description": "相同渐变背景。不对称布局：右侧是大型磨砂玻璃面板，用粗体字展示指标。左侧：由玻璃面板和连接线条构成的抽象3D地球，代表全球布局。浮动的小型玻璃卡片作为数据可视化元素，显示数字。整体充满柔和环境光。保持高级科技美学。"
    },
    {
      "slide_number": 5,
      "type": "conclusion",
      "title": "未来，即刻开启",
      "subtitle": "加入等候名单",
      "visual_description": "戏剧化的终页。渐变背景略微提升饱和度。中央磨砂玻璃卡片带有粗体标题'未来，即刻开启'和行动号召副标题。卡片后方：柔和光线射线爆发和浮动玻璃粒子营造庆祝效果。多层玻璃形状营造深度。在保持风格一致性的同时成为视觉冲击力最强的页面。"
    }
  ]
}
```

### 步骤2：读取图像生成技能

调用MCP工具进行图像生成。

### 步骤3：按顺序生成幻灯片图像，保持统一seed

**第1页 - 封面（确立视觉语言）：**
创建`/home/LinXuan/Downloads/nova-slide-01.json`：

```json
{
  "prompt": "Ultra-premium presentation title slide with glassmorphism design. Background: smooth flowing gradient from deep purple (#667eea) through magenta (#f093fb) to cyan (#00d4ff), soft and vibrant. Center: large frosted glass panel with strong backdrop blur effect, rounded corners 32px, containing bold white sans-serif title 'Introducing Nova AI' (72pt, SF Pro Display style, font-weight 700) with subtle text shadow, subtitle 'Intelligence, Reimagined' below in lighter weight. The glass panel has subtle white border (1px rgba 255,255,255,0.25) and soft purple-tinted drop shadow. Floating around the card: 3D glass spheres with refraction, translucent geometric shapes (icosahedrons, abstract blobs), creating depth and dimension. Soft luminous glow emanating from behind the glass panel. Small floating particles of light. Apple Vision Pro / visionOS UI aesthetic. Professional presentation slide, 16:9 aspect ratio. Hyper-modern, premium tech product launch feel.",
  "style": "Glassmorphism, visionOS aesthetic, Apple Vision Pro UI style, premium tech, 2024 design trends",
  "composition": "Centered glass card as focal point, floating 3D elements creating depth at edges, 40% negative space, clear visual hierarchy",
  "lighting": "Soft ambient glow from gradient, light refraction through glass elements, subtle rim lighting on 3D shapes",
  "color_palette": "Purple gradient #667eea, magenta #f093fb, cyan #00d4ff, frosted white rgba(255,255,255,0.15), pure white text #ffffff",
  "effects": "Backdrop blur on glass panels, soft drop shadows with color tint, light refraction, subtle noise texture on glass, floating particles"
}
```

```bash
# 1. 使用 tongyi_wanx-t2i-image-generation 工具提交生图任务，设置 prompt, negative_prompt 和相同的 seed (如 12345)
# 2. 使用 tongyi_wanx-t2i-image-generation-result 工具轮询获取图片 URL
# 3. 下载图片到本地的 Downloads 目录
curl -s -o /home/LinXuan/Downloads/slide-0X.jpg "获取到的URL"
```

**第2页 - 内容页（必须引用第1页保证一致性）：**

创建`/home/LinXuan/Downloads/nova-slide-02.json`：

```json
{
  "prompt": "Presentation slide continuing EXACT visual style from reference image. SAME purple-to-cyan gradient background, SAME glassmorphism aesthetic, SAME typography style. Left side: frosted glass card with backdrop blur containing title 'Why Nova?' in bold white (matching reference font style), three feature points as subtle glass pill badges below. Right side: abstract 3D neural network visualization made of interconnected glass nodes with soft cyan glow, floating in space. Floating translucent geometric shapes (matching style from reference) adding depth. The frosted glass has identical treatment: white border, purple-tinted shadow, same blur intensity. CRITICAL: This slide must look like it belongs in the exact same presentation as the reference image - same colors, same glass treatment, same overall aesthetic.",
  "style": "MATCH REFERENCE EXACTLY - Glassmorphism, visionOS aesthetic, same visual language",
  "composition": "Asymmetric split: glass card left (40%), 3D visualization right (40%), breathing room between elements",
  "color_palette": "EXACTLY match reference: purple #667eea, cyan #00d4ff gradient, same frosted white treatment, same text white",
  "consistency_note": "CRITICAL: Must be visually identical in style to reference image. Same gradient colors, same glass blur intensity, same shadow treatment, same typography weight and style. Viewer should immediately recognize this as the same presentation."
}
```

```bash
# 1. 使用 tongyi_wanx-t2i-image-generation 工具提交生图任务，设置 prompt, negative_prompt 和相同的 seed (如 12345)
# 2. 使用 tongyi_wanx-t2i-image-generation-result 工具轮询获取图片 URL
# 3. 下载图片到本地的 Downloads 目录
curl -s -o /home/LinXuan/Downloads/slide-0X.jpg "获取到的URL"
```

**第3-5页：沿用相同模式，每页引用前一页**
后续页面核心一致性规则：

* 提示词中始终包含「完全延续参考图像的视觉风格」
* 明确指定「相同渐变背景」、「相同玻璃效果处理」、「相同字体风格」
* 加入`consistency_note`字段强调风格匹配要求
* 使用相同的seed

### 步骤4：合成最终PPT

```bash
python /home/LinXuan/.config/opencode/skills/ppt-generation/scripts/generate.py \
  --plan-file /home/LinXuan/Downloads/nova-plan.json \
  --slide-images /home/LinXuan/Downloads/nova-slide-01.jpg /home/LinXuan/Downloads/nova-slide-02.jpg /home/LinXuan/Downloads/nova-slide-03.jpg /home/LinXuan/Downloads/nova-slide-04.jpg /home/LinXuan/Downloads/nova-slide-05.jpg \
  --output-file /home/LinXuan/Downloads/nova-presentation.pptx
```

## 各风格专属指南

### 玻璃态风格（推荐 - 最现代前卫）

```json
{
  "style": "glassmorphism",
  "style_guidelines": {
    "color_palette": "活力渐变背景（紫色#667eea到粉色#f093fb，或青色#4facfe到蓝色#00f2fe）、20%透明度的磨砂白色面板、在渐变背景上醒目的强调色",
    "typography": "SF Pro Display或Inter字体风格、600-700粗体标题、400字重清晰正文、白色文字加微妙阴影保证在玻璃上的可读性",
    "imagery": "悬浮的抽象3D形状、柔和模糊球体、玻璃材质的几何基础图形、通过重叠半透明层营造深度感",
    "layout": "带背景模糊效果的浮动卡片面板、充足内边距(48-64px)、圆角(24-32px半径)、通过微妙阴影营造分层深度",
    "effects": "毛玻璃模糊（backdrop-filter: blur 20px）、微妙白色边框(1px rgba 255,255,255,0.2)、面板后柔光效果、带阴影的浮动元素",
    "visual_language": "苹果Vision Pro/visionOS UI美学、通过透明度营造深度感、光线穿过玻璃表面的折射效果"
  }
}
```

### 暗黑高端风格

```json
{
  "style": "dark-premium",
  "style_guidelines": {
    "color_palette": "深黑色底色(#0a0a0a到#121212)、亮色调强调色（电光蓝#00d4ff、霓虹紫#bf5af2或金色#ffd700）、微妙灰度渐变营造深度感(#1a1a1a到#0a0a0a)",
    "typography": "优雅无衬线字体（Neue Haas Grotesk或Suisse Int'l风格）、夸张的字号对比（72pt+标题、18pt正文）、标题字距-0.02em、纯白色(#ffffff)文字",
    "imagery": "戏剧化的布光、轮廓光和边缘发光、影院级产品摄影、抽象光轨、高端材质纹理（拉丝金属、哑光表面）",
    "layout": "大量留白（60%+）、不对称平衡、内容锚定网格但留有呼吸空间、每页单焦点",
    "effects": "关键元素后的微妙环境光、光晕效果、2-3%不透明度的颗粒纹理叠加、边缘暗角",
    "visual_language": "奢侈品科技品牌美学（Bang & Olufsen、保时捷设计）、克制体现精致感、每个元素都经过精心设计"
  }
}
```

### 渐变现代风格

```json
{
  "style": "gradient-modern",
  "style_guidelines": {
    "color_palette": "大胆的网格渐变（Stripe/Linear风格：紫-粉-橙#7c3aed→#ec4899→#f97316，或冷色调：青-蓝-紫#06b6d4→#3b82f6→#8b5cf6）、根据背景强度选择白色或深色文字",
    "typography": "现代几何无衬线字体（Satoshi、General Sans或Clash Display风格）、可变字重、超大粗体标题（80pt+）、舒适的20pt正文",
    "imagery": "抽象流体形状、渐变变形、3D渲染抽象物体、柔和有机形态、浮动几何基础图形",
    "layout": "动态不对称构图、带混合模式的重叠元素、文字与渐变融合、全出血背景",
    "effects": "平滑渐变过渡、3-5%不透明度的微妙颗粒纹理增加深度、带渐变色调的柔和阴影、暗示动感的运动模糊",
    "visual_language": "现代SaaS美学（Stripe、Linear、Vercel）、充满活力但专业、前瞻性科技感"
  }
}
```

### 新粗野主义风格

```json
{
  "style": "neo-brutalist",
  "style_guidelines": {
    "color_palette": "高对比度原色：纯黑、纯白、加一个醒目的强调色（热粉色#ff0080、电光黄#ffff00或正红色#ff0000）、可选：孟菲斯风格的柔和浅色作为次要颜色",
    "typography": "超粗压缩字体（Impact、Druk或Bebas Neue风格）、全大写标题、极端字号对比、刻意紧凑或重叠的字间距",
    "imagery": "未经过滤的原始摄影、刻意的视觉噪点、半色调图案、拼贴切割美学、手绘元素、贴纸和印章效果",
    "layout": "打破网格、重叠元素、4-8px粗黑边框、结构可见、反留白设计（密集但有组织的混乱感）",
    "effects": "硬阴影（无模糊，偏移8-12px）、像素化装饰、扫描线、CRT屏幕效果、刻意的「错误」设计",
    "visual_language": "反企业叛逆感、DIY杂志美学与数字结合、原生真实感、通过大胆设计令人印象深刻"
  }
}
```

### 3D等距风格

```json
{
  "style": "3d-isometric",
  "style_guidelines": {
    "color_palette": "柔和现代调色板：低饱和度紫色(#8b5cf6)、青色(#14b8a6)、暖珊瑚色(#fb7185)、搭配奶油色或浅灰色背景(#fafafa)、所有元素饱和度一致",
    "typography": "友好的几何无衬线字体（Circular、Gilroy或Quicksand风格）、中等字重标题、极佳可读性、舒适的24pt正文",
    "imagery": "简洁的等距3D插图、统一30°等距视角、柔和粘土渲染美学、浮动平台和设备、可爱的简化物体",
    "layout": "中央等距场景作为核心、文字围绕3D元素平衡排布、清晰视觉层级、舒适边距（64px+）",
    "effects": "柔和投影（20px模糊、30%不透明度）、3D物体的环境光遮蔽、表面的微妙渐变、统一光源（左上方向）",
    "visual_language": "友好的科技插图风格（Slack、Notion、Asana风格）、平易近人的复杂度、通过简化实现清晰表达"
  }
}
```

### 杂志编辑风格

```json
{
  "style": "editorial",
  "style_guidelines": {
    "color_palette": "精致中性色：米白色(#f5f5f0)、炭黑色(#2d2d2d)、搭配单一强调色（勃艮第红#7c2d12、森林绿#14532d或海军蓝#1e3a5f）、偶尔使用全彩摄影",
    "typography": "精致衬线字体用于标题（Playfair Display、Freight或Editorial New风格）、简洁无衬线用于正文（Söhne、Graphik）、戏剧化的字号层级（96pt标题、16pt正文）、宽松行高1.6",
    "imagery": "杂志级摄影、戏剧化裁剪、全出血图像、带刻意留白的人像、杂志级布光（Vogue、彭博商业周刊风格）",
    "layout": "精致网格系统（12列）、刻意的不对称布局、引用语作为设计元素、文字环绕图片、优雅边距",
    "effects": "极简效果 - 让摄影和排版本身发光、微妙图像处理（轻微去饱和、胶片颗粒）、优雅边框和分隔线",
    "visual_language": "高端杂志美学、知识分子气质、通过设计克制提升内容质感"
  }
}
```

### 极简瑞士风格

```json
{
  "style": "minimal-swiss",
  "style_guidelines": {
    "color_palette": "纯白色(#ffffff)或米白色(#fafaf9)背景、纯黑色(#000000)文字、单一醒目的强调色（瑞士红#ff0000、克莱因蓝#002fa7或信号黄#ffcc00）",
    "typography": "Helvetica Neue或Aktiv Grotesk字体、严格的字号比例(12/16/24/48/96)、正文用中等字重、仅在强调时用粗体、左对齐右不对齐排版",
    "imagery": "客观摄影、几何形状、简洁图标、数学精度、刻意留白作为构图元素",
    "layout": "严格遵守网格（精神上对齐基线网格）、模块化构图、大量留白（40%+页面占比）、内容对齐不可见网格线",
    "effects": "无 - 形式纯粹、无阴影、无渐变、无装饰元素、偶尔使用细单像素分隔线",
    "visual_language": "国际印刷风格、形式追随功能、永恒现代主义、迪特·拉姆斯式克制设计"
  }
}
```

### Keynote风格（苹果风格）

```json
{
  "style": "keynote",
  "style_guidelines": {
    "color_palette": "深黑色(#000000到#1d1d1f)、纯白色文字、标志性蓝色(#0071e3)或渐变强调色（创意主题用紫-粉渐变、科技主题用青-蓝渐变）",
    "typography": "San Francisco Pro Display字体、极端字重对比（80pt+粗体标题、24pt细体正文）、标题负字距(-0.03em)、视觉对齐",
    "imagery": "影院级摄影、浅景深、戏剧化布光（轮廓光、聚光）、带反射的产品英雄图、全出血图像",
    "layout": "最大化留白、每页单张有冲击力的图像或单条核心信息、内容居中或戏剧化偏移、无冗余元素",
    "effects": "微妙渐变叠加、关键元素上的光晕和发光效果、表面反射、平滑渐变背景",
    "visual_language": "苹果WWDC主题演讲美学、通过简洁传递自信、每个像素都经过精心设计、剧场级呈现效果"
  }
}
```

## 输出处理

生成完成后：

* PPTX文件保存在`/home/LinXuan/Downloads/`目录
* 如果用户要求，也可以分享单独的幻灯片图像
* 提供演示文稿的简要说明
* 如果需要，提供迭代或重新生成特定页面的选项

## 注意事项

### 核心质量规范

**专业效果提示词工程：**

* 无论用户使用什么语言，图像提示词始终使用英文
* 对视觉细节描述要**极度具体** - 模糊的提示词会产生通用平庸的结果
* 包含精确的十六进制颜色代码（例如#667eea，而不是「紫色」）
* 指定排版细节：字体粗细（400/700）、字号层级、字间距
* 精确描述效果：「背景模糊20px」、「投影8px模糊、30%不透明度」
* 参考真实设计系统：「visionOS美学」、「Stripe网站风格」、「彭博商业周刊布局」

**视觉一致性（最重要）：**

* **按顺序生成幻灯片** - 每一页必须引用前一页
* 第一页至关重要 - 它确立了整个演示文稿的视觉语言
* 每个后续页面的提示词中都要明确声明：「完全延续参考图像的视觉风格」
* 在提示词中主动使用「相同」、「完全一致」、「匹配」等关键词强化一致性要求
* 第1页之后的每个JSON提示词中都要包含`consistency_note`字段
* 如果某一页看起来风格不一致，使用更强的参考强调重新生成

**现代美学设计原则：**

* 善用留白 - 40-60%的留白能营造高级感
* 每页元素精简 - 单焦点、单信息
* 通过分层营造深度（阴影、透明度、z轴层级）
* 排版层级：超大标题（72pt+）、舒适正文（18-24pt）
* 色彩克制：单一主色调、最多1-2个强调色

**需要避免的常见错误：**

* ❌ 模糊的提示词如「专业幻灯片」 - 务必具体描述
* ❌ 每页元素/文字过多 - 杂乱 = 不专业
* ❌ 页面之间颜色不一致 - 始终引用前一页
* ❌ 省略参考图像参数 - 会破坏视觉一致性
* ❌ 同一演示文稿中使用不同设计风格
* ❌ 并行生成幻灯片 - 必须按顺序逐页生成（第1页→第2页→第3页...），绝对禁止同时生成多页

**不同场景推荐风格：**

* 科技产品发布会 → `玻璃态风格`或`渐变现代风`
* 奢侈品/高端品牌 → `暗黑高端风`或`杂志编辑风`
* 创业项目路演 → `渐变现代风`或`极简瑞士风`
* 高管汇报 → `暗黑高端风`或`Keynote风格`
* 创意机构展示 → `新粗野主义风`或`渐变现代风`
* 数据/分析报告 → `极简瑞士风`或`3D等距风格`
