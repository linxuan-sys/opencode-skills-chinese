# Skills 技能集合

一套面向 AI Agent 的技能（Skills）集合，共 **17 个技能**。

每个技能以 `SKILL.md` 为核心文档，为 Agent 定义特定领域的任务流程、操作规范与配套工具。将技能安装到你的 Agent 后，Agent 会在合适的任务中自动触发对应技能。

## 使用方法

这些技能采用通用的 **Agent Skills** 格式（每个技能是一个目录，核心为 `SKILL.md`，其 frontmatter 包含 `name` 与 `description`），**不绑定特定平台——所有支持 Skills 的 Agent 均可直接使用**，包括 OpenCode、Claude Code 等。

将技能目录放入对应 Agent 的技能文件夹即可被自动加载，一些常用 Agent 的全局技能目录如下：

| 工具 | 技能目录 |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| ZCode | `~/.zcode/skills/` |
| Codex | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| Cline | `~/.agents/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |
| Goose | `~/.config/goose/skills/` |
| Continue | `~/.continue/skills/` |
| Roo Code | `~/.roo/skills/` |
| Kimi Code CLI | `~/.config/agents/skills/` |
| OpenHands | `~/.openhands/skills/` |

> 上表为各工具的全局（用户级）技能目录，具体以各工具官方文档为准；多数工具同时支持项目级技能目录。

每个技能目录包含：

- **SKILL.md** — 技能主文档：名称、描述、触发条件与操作说明
- **辅助文件** — 脚本、参考文档、模板、主题、字体等资源（视技能而定）

## 技能总览

| 分类 | 技能 |
| --- | --- |
| 📄 文档处理 | docx · pdf · pptx · xlsx |
| 🎨 设计与创作 | canvas-design · algorithmic-art · frontend-design · chart-generator · theme-factory |
| 💻 开发与调试 | code-reviewer · mcp-builder · systematic-debugging · playwright-cli · agent-qa |
| 📝 写作与协作 | doc-coauthoring |
| 🔧 系统与元技能 | arch-system-troubleshooter · skill-creator |

---

## 📄 文档处理

### docx — Word 文档创建与编辑

**作用**：创建、读取、编辑、操作 Word 文档（.docx）。支持生成带目录、标题、页码、信头格式的专业文档；从 .docx 提取或重组内容、插入或替换图片、查找替换、处理修订与评论，并将内容转换为精美的 Word 交付物。

**触发场景**：任何提及 Word / .docx 的任务；要求生成"报告 / 备忘录 / 信件 / 模板"等 Word 交付物。

**附带资源**：`scripts/` — 文档解包 / 打包 / 校验、批注与修订处理、LibreOffice 调度等脚本。

### pdf — PDF 全能处理

**作用**：读取或提取 PDF 文本 / 表格；合并、拆分、旋转页面；添加水印；创建新 PDF；填写 PDF 表单；加密 / 解密；提取图片；对扫描版 PDF 进行 OCR 使其可搜索。

**触发场景**：任何涉及 .pdf 文件的读取、转换、生成或编辑任务。

**附带资源**：`scripts/` — 表单字段检查与填写、表单结构提取、PDF 转图片等脚本；`reference.md` — 高级用法；`forms.md` — 表单填写指南。

### pptx — PowerPoint 演示文稿

**作用**：创建幻灯片 / 演示文稿；读取、解析或提取 .pptx 中的文本；编辑、修改、更新现有演示文稿；合并或拆分幻灯片文件；处理模板、布局、演讲者备注与批注。

**触发场景**：任何涉及 .pptx 的任务；提到 deck / slides / presentation 时。

**附带资源**：`scripts/` — 幻灯片清理 / 增删、缩略图、Office 打包校验套件；`editing.md` — 基于模板编辑指南；`pptxgenjs.md` — 从零创建指南。

### xlsx — Excel 电子表格

**作用**：打开、读取、编辑、修复 .xlsx / .xlsm / .csv / .tsv；添加列、计算公式、格式化、制作图表、清理杂乱数据；从零创建电子表格；在表格类格式间转换；将错行、错表头、垃圾数据整理为规范表格。

**触发场景**：电子表格文件作为主要输入或输出时；按名称或路径引用表格文件时。

**附带资源**：`scripts/` — 公式重算、Office 打包校验套件。

---

## 🎨 设计与创作

### canvas-design — 视觉设计

**作用**：以"设计哲学"驱动创作，在 .png 和 .pdf 文档中输出精美的视觉艺术，适合从零设计而非套模板，确保视觉统一与原创性。

**触发场景**：要求创建海报、艺术品、设计稿或其他静态视觉作品。

**附带资源**：`canvas-fonts/` — 一批精选开源字体。

### algorithmic-art — 算法艺术

**作用**：使用 p5.js 创作带种子随机与交互式参数探索的算法艺术：流场、粒子系统、生成艺术。强调原创，不复制已有艺术家的作品。

**触发场景**：要求用代码创建艺术 / 生成艺术 / 算法艺术 / 流场 / 粒子系统。

**产出**：算法哲学 .md + 交互式查看器 .html + 生成算法 .js；`templates/` — 起步模板。

### frontend-design — 前端界面设计

**作用**：创建独具特色、达到生产级质量的前端界面：落地页、仪表盘、应用外壳、组件、视觉系统。避免"通用 AI 风"UI，强调清晰的设计方向与完整执行。

**触发场景**：构建 Web 组件 / 页面 / 应用，且视觉效果与代码质量同等重要时。

### chart-generator — 数据可视化

**作用**：按照自定义的 matplotlib 规范或 antv MCP 工具生成各类可视化图表：柱状图、折线图、饼图、散点图、雷达图、面积图等。

**触发场景**：提到生成图表、可视化数据时。

### theme-factory — 主题样式工厂

**作用**：为幻灯片、文档、报告、HTML 落地页等各种成品套用专业配色与字体主题。内置 10 套精选主题，也可以即时生成新主题。

**触发场景**：给已完成的工件统一视觉样式时。

**附带资源**：`themes/` — 10 套主题定义；`theme-showcase.pdf` — 主题效果预览。

---

## 💻 开发与调试

### code-reviewer — 代码审查

**作用**：从五大维度审查代码，输出分级问题报告与质量评分：1. 安全漏洞 2. 性能问题 3.结构与冗余性（发现冗余代码会醒目提示，帮你删掉重复和无用的功能）4. 正确性与健壮性 5. 最佳实践与可读性

**触发场景**：代码审查、安全审计、代码质量检查、PR 审查、代码瘦身与重构评估。

### mcp-builder — MCP 服务器开发

**作用**：构建高质量 MCP（模型上下文协议）服务器的完整指南，使 LLM 能通过精心设计的工具与外部服务交互。覆盖研究规划、实现、测试评估全流程，支持 Python（FastMCP）与 Node/TypeScript（MCP SDK）。

**触发场景**：构建 MCP 服务器以集成外部 API 或服务时。

**附带资源**：`reference/` — 各语言指南与评估方法；`scripts/` — 辅助脚本。

### systematic-debugging — 系统化调试

**作用**：一套严谨的调试方法论。核心铁律：**未先完成根本原因调查，绝不提出修复方案**。提供根因追踪、条件式等待、纵深防御等具体技巧。

**触发场景**：遇到任何 bug、测试失败或意外行为时。

**附带资源**：多篇方法论文档（根因追踪、条件式等待、纵深防御等）与压力测试材料。

### playwright-cli — 浏览器自动化

**作用**：自动化浏览器交互、测试网页、处理 Playwright 测试用例。浏览器默认以可见窗口模式运行，支持快照式元素交互、会话管理、视频录制、请求模拟等。

**触发场景**：浏览器自动化、网页测试、表单交互、截图快照。

**附带资源**：`references/` — 会话管理、视频录制、存储状态、追踪、请求模拟、测试生成等专题文档。

### agent-qa — 应用回归与证据复核

**作用**：使用 vostride 的 agent-qa 运行选定回归测试并检查证据；借助先进的 memidex 记忆引擎与自我改进能力，复用经验并追溯结论来源。

**触发场景**：已有 agent-qa 项目的应用回归、失败分析、运行结果复核与记忆来源检查。

**技能文档**：[agent-qa/SKILL.md](agent-qa/SKILL.md)。

---

## 📝 写作与协作

### doc-coauthoring — 文档协作工作流

**作用**：引导完成三阶段结构化文档协作：① 上下文收集 → ② 优化与结构化 → ③ 读者测试（用全新、无上下文的 Agent 试读文档，在他人阅读之前发现盲点）。

**触发场景**：编写文档、提案、技术规范、决策文档、PRD、RFC 等结构化内容时。

---

## 🔧 系统与元技能

### arch-system-troubleshooter — Arch Linux 故障排查

**作用**：排查 Arch Linux 系统的各类故障：滚挂、报错、niri 配置问题、命令异常等。严格执行排查顺序——本地系统文档 → Arch Wiki → 网络搜索，优先返回官方解决方案。

**触发场景**：提到系统故障、报错、命令不对、niri / Arch 配置异常时。

### skill-creator — 技能创建器

**作用**：从头创建新技能、修改与优化现有技能；运行 eval 测试、通过方差分析对技能性能进行基准测试、优化技能描述以提高触发准确率。内含完整的"撰写 → 测试 → 评估 → 迭代"闭环流程。

**触发场景**：创建 / 编辑 / 优化技能，或对技能进行评测时。

**附带资源**：`agents/` — 对比 / 评分 / 分析子代理；`eval-viewer/` — 评测结果查看器；`references/` — 规范文档；`scripts/`、`assets/`。

---

## 许可证

本项目基于 [MIT 许可证](LICENSE) 发布。
