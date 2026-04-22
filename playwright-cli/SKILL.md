---
name: playwright-cli
description: 自动化浏览器交互、测试网页以及处理Playwright测试用例
allowed-tools: Bash(playwright-cli:*) Bash(npx:*) Bash(npm:*)
---

# playwright-cli 浏览器自动化工具
> 🔴 ⚠️ 【强制规则，必须遵守】⚠️ 🔴
> 🔴 所有调用`playwright-cli open`的命令，必须默认加上`--headed`参数！
> 🔴 仅用户明确要求使用无头模式时，才可去掉该参数！
> 🔴 禁止后台静默运行浏览器，必须显示窗口！

## 快速入门

```bash
# 打开新浏览器
playwright-cli open
# 跳转到指定页面
playwright-cli goto https://playwright.dev
# 使用快照中的元素引用与页面交互
playwright-cli click e15
playwright-cli type "page.click"
playwright-cli press Enter
# 截图（较少使用，快照功能更常用）
playwright-cli screenshot
# 关闭浏览器
playwright-cli close
```

## 命令说明

### 核心命令

```bash
playwright-cli open
# 打开浏览器并直接跳转到指定url
playwright-cli open https://example.com/
playwright-cli goto https://playwright.dev
playwright-cli type "搜索关键词"
playwright-cli click e3
playwright-cli dblclick e7
# --submit参数会在填充元素后自动按回车提交
playwright-cli fill e5 "user@example.com"  --submit
playwright-cli drag e2 e8
playwright-cli hover e4
playwright-cli select e9 "选项值"
playwright-cli upload ./document.pdf
playwright-cli check e12
playwright-cli uncheck e12
playwright-cli snapshot
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
# 获取快照中不显示的元素id、class或其他属性
playwright-cli eval "el => el.id" e5
playwright-cli eval "el => el.getAttribute('data-testid')" e5
playwright-cli dialog-accept
playwright-cli dialog-accept "确认文本"
playwright-cli dialog-dismiss
playwright-cli resize 1920 1080
playwright-cli close
```

### 导航命令

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

### 键盘命令

```bash
playwright-cli press Enter
playwright-cli press ArrowDown
playwright-cli keydown Shift
playwright-cli keyup Shift
```

### 鼠标命令

```bash
playwright-cli mousemove 150 300
playwright-cli mousedown
playwright-cli mousedown right
playwright-cli mouseup
playwright-cli mouseup right
playwright-cli mousewheel 0 100
```

### 导出命令

```bash
playwright-cli screenshot
playwright-cli screenshot e5
playwright-cli screenshot --filename=page.png
playwright-cli pdf --filename=page.pdf
```

### 标签页命令

```bash
playwright-cli tab-list
playwright-cli tab-new
playwright-cli tab-new https://example.com/page
playwright-cli tab-close
playwright-cli tab-close 2
playwright-cli tab-select 0
```

### 存储命令

```bash
playwright-cli state-save
playwright-cli state-save auth.json
playwright-cli state-load auth.json

# Cookie操作
playwright-cli cookie-list
playwright-cli cookie-list --domain=example.com
playwright-cli cookie-get session_id
playwright-cli cookie-set session_id abc123
playwright-cli cookie-set session_id abc123 --domain=example.com --httpOnly --secure
playwright-cli cookie-delete session_id
playwright-cli cookie-clear

# LocalStorage操作
playwright-cli localstorage-list
playwright-cli localstorage-get theme
playwright-cli localstorage-set theme dark
playwright-cli localstorage-delete theme
playwright-cli localstorage-clear

# SessionStorage操作
playwright-cli sessionstorage-list
playwright-cli sessionstorage-get step
playwright-cli sessionstorage-set step 3
playwright-cli sessionstorage-delete step
playwright-cli sessionstorage-clear
```

### 网络命令

```bash
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
playwright-cli route-list
playwright-cli unroute "**/*.jpg"
playwright-cli unroute
```

### 开发者工具命令

```bash
playwright-cli console
playwright-cli console warning
playwright-cli network
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli run-code --filename=script.js
playwright-cli tracing-start
playwright-cli tracing-stop
playwright-cli video-start video.webm
playwright-cli video-chapter "章节标题" --description="详细说明" --duration=2000
playwright-cli video-stop
```

## 原始输出模式

全局参数`--raw`会去掉页面状态、生成代码和快照部分的输出，仅返回结果值，适合将命令输出管道到其他工具使用。没有输出的命令执行后不会返回任何内容。

```bash
playwright-cli --raw eval "JSON.stringify(performance.timing)" | jq '.loadEventEnd - .navigationStart'
playwright-cli --raw eval "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href))" > links.json
playwright-cli --raw snapshot > before.yml
playwright-cli click e5
playwright-cli --raw snapshot > after.yml
diff before.yml after.yml
TOKEN=$(playwright-cli --raw cookie-get session_id)
playwright-cli --raw localstorage-get theme
```

## 启动参数
```bash
# 启动时指定使用的浏览器，可选值：chrome, firefox, webkit, msedge
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit
playwright-cli open --browser=msedge

# 使用持久化浏览器配置文件（默认使用内存中的临时配置，关闭后清空所有数据）
playwright-cli open --persistent
# 自定义持久化配置文件的存储目录
playwright-cli open --profile=/path/to/profile

# 通过扩展连接到浏览器
playwright-cli attach --extension

# 通过通道名连接到正在运行的Chrome或Edge
playwright-cli attach --cdp=chrome
playwright-cli attach --cdp=msedge

# 通过CDP端点连接到正在运行的浏览器
playwright-cli attach --cdp=http://localhost:9222

# 从指定配置文件启动
playwright-cli open --config=my-config.json

# 关闭浏览器
playwright-cli close
# 删除默认会话的用户数据
playwright-cli delete-data
```

## 快照功能

每次命令执行后，playwright-cli都会返回当前浏览器状态的快照。

```bash
> playwright-cli goto https://example.com
### 页面信息
- 页面URL: https://example.com/
- 页面标题: Example Domain
### 快照
[Snapshot](.playwright-cli/page-2026-02-14T19-22-42-679Z.yml)
```

你也可以按需手动执行`snapshot`命令获取快照，所有参数可以组合使用：

```bash
# 默认保存到按时间戳命名的文件
playwright-cli snapshot

# 保存到指定文件，适合工作流结果中使用快照
playwright-cli snapshot --filename=after-click.yaml

# 仅快照指定元素而非整个页面
playwright-cli snapshot "#main"

# 限制快照的深度提升效率，之后可以对指定元素单独快照
playwright-cli snapshot --depth=4
playwright-cli snapshot e34
```

## 元素定位

默认使用快照中的元素引用（比如e15这种形式）来和页面元素交互。

```bash
# 获取带元素引用的快照
playwright-cli snapshot

# 使用元素引用进行交互
playwright-cli click e15
```

你也可以使用css选择器或者Playwright内置选择器：

```bash
# css选择器
playwright-cli click "#main > button.submit"

# 角色选择器
playwright-cli click "getByRole('button', { name: 'Submit' })"

# 测试ID选择器
playwright-cli click "getByTestId('submit-button')"
```

## 浏览器会话

```bash
# 创建名为mysession的新浏览器会话，使用持久化配置
playwright-cli -s=mysession open example.com --persistent
# 手动指定配置文件目录（需要时使用）
playwright-cli -s=mysession open example.com --profile=/path/to/profile
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close  # 停止指定名称的浏览器会话
playwright-cli -s=mysession delete-data  # 删除持久化会话的用户数据

playwright-cli list
# 关闭所有浏览器
playwright-cli close-all
# 强制终止所有浏览器进程
playwright-cli kill-all
```

## 安装说明

如果全局`playwright-cli`命令不可用，可以尝试通过npx使用本地版本：

```bash
npx --no-install playwright-cli --version
```

如果本地版本可用，所有命令都可以用`npx playwright-cli`代替。否则可以全局安装playwright-cli：

```bash
npm install -g @playwright/cli@latest
```

## 示例：表单提交

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot

playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
playwright-cli snapshot
playwright-cli close
```

## 示例：多标签页工作流

```bash
playwright-cli open https://example.com
playwright-cli tab-new https://example.com/other
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli snapshot
playwright-cli close
```

## 示例：使用开发者工具调试

```bash
playwright-cli open https://example.com
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli console
playwright-cli network
playwright-cli close
```

```bash
playwright-cli open https://example.com
playwright-cli tracing-start
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli tracing-stop
playwright-cli close
```

## 特定场景用法

* **运行和调试Playwright测试用例** [references/playwright-tests.md](references/playwright-tests.md)
* **请求Mock** [references/request-mocking.md](references/request-mocking.md)
* **运行Playwright代码** [references/running-code.md](references/running-code.md)
* **浏览器会话管理** [references/session-management.md](references/session-management.md)
* **存储状态（Cookie、localStorage）** [references/storage-state.md](references/storage-state.md)
* **测试用例生成** [references/test-generation.md](references/test-generation.md)
* **链路追踪** [references/tracing.md](references/tracing.md)
* **视频录制** [references/video-recording.md](references/video-recording.md)
* **元素属性检查** [references/element-attributes.md](references/element-attributes.md)
