---
name: opencode
description: 将编码任务委托给OpenCode CLI代理，用于功能实现、代码重构、PR审查和长时间自动会话。需要提前安装并认证OpenCode CLI。
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [编码代理, OpenCode, 自动化, 代码重构, 代码审查]
    related_skills: [claude-code, codex, hermes-agent]
---

# OpenCode CLI

使用 [OpenCode](https://opencode.ai) 作为由Hermes终端/进程工具编排的自动编码助手。OpenCode是一个不绑定服务商的开源AI编码代理，提供终端界面(TUI)和命令行界面(CLI)。

## 适用场景

* 用户明确要求使用OpenCode
* 需要外部编码代理实现/重构/审查代码
* 需要带进度检查的长时间编码会话
* 需要在独立工作目录/工作树中并行执行任务

## 前置条件

* 已安装OpenCode：`npm i -g opencode-ai@latest` 或 `brew install anomalyco/tap/opencode`
* 已配置认证：`opencode auth login` 或设置服务商环境变量（OPENROUTER_API_KEY等）
* 验证配置：`opencode auth list` 应显示至少一个可用服务商
* 编码任务推荐在Git仓库中执行
* 交互式TUI会话需要设置`pty=true`

## 二进制路径解析（重要）

不同Shell环境可能解析到不同的OpenCode二进制文件。如果终端中和Hermes中的行为不一致，请检查：

```
terminal(command="which -a opencode")
terminal(command="opencode --version")
```

如果需要，可以指定明确的二进制路径：

```
terminal(command="$HOME/.opencode/bin/opencode run '...'", workdir="~/project", pty=true)
```

## 一次性任务

使用`opencode run`执行有明确边界的非交互式任务：

```
terminal(command="opencode run '给API调用添加重试逻辑并更新测试'", workdir="~/project")
```

使用`-f`附加上下文文件：

```
terminal(command="opencode run '审查此配置的安全问题' -f config.yaml -f .env.example", workdir="~/project")
```

使用`--thinking`显示模型的思考过程：

```
terminal(command="opencode run '调试CI中测试失败的原因' --thinking", workdir="~/project")
```

强制使用指定模型：

```
terminal(command="opencode run '重构认证模块' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

## 交互式会话（后台运行）

对于需要多次交互的迭代工作，可以后台启动TUI界面：

```
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# 返回会话ID

# 发送任务指令
process(action="submit", session_id="<id>", data="实现OAuth刷新流程并添加测试")

# 监控进度
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# 发送后续指令
process(action="submit", session_id="<id>", data="现在添加令牌过期的错误处理")

# 优雅退出 — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# 或直接杀死进程
process(action="kill", session_id="<id>")
```

**重要：** 不要使用`/exit`命令 — 这不是有效的OpenCode命令，会打开代理选择对话框。使用Ctrl+C(`\x03`)或`process(action="kill")`退出。

### TUI快捷键

| 按键 | 功能 |
|-----|--------|
| `Enter` | 提交消息（如需按两次） |
| `Tab` | 切换代理（构建/规划） |
| `Ctrl+P` | 打开命令面板 |
| `Ctrl+X L` | 切换会话 |
| `Ctrl+X M` | 切换模型 |
| `Ctrl+X N` | 新建会话 |
| `Ctrl+X E` | 打开编辑器 |
| `Ctrl+C` | 退出OpenCode |

### 恢复会话

退出后，OpenCode会打印会话ID。使用以下命令恢复：

```
terminal(command="opencode -c", workdir="~/project", background=true, pty=true)  # 继续上次会话
terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)  # 恢复指定会话
```

## 常用参数

| 参数 | 用途 |
|------|-----|
| `run '提示词'` | 一次性执行任务后退出 |
| `--continue` / `-c` | 继续上一次OpenCode会话 |
| `--session <id>` / `-s` | 继续指定会话 |
| `--agent <name>` | 选择OpenCode代理（build或plan） |
| `--model 服务商/模型` | 强制使用指定模型 |
| `--format json` | 机器可读输出/事件格式 |
| `--file <路径>` / `-f` | 附加文件到消息中 |
| `--thinking` | 显示模型思考过程 |
| `--variant <级别>` | 推理强度（high、max、minimal） |
| `--title <名称>` | 为会话命名 |
| `--attach <url>` | 连接到正在运行的opencode服务器 |

## 使用流程

1. 验证工具就绪：
   * `terminal(command="opencode --version")`
   * `terminal(command="opencode auth list")`
2. 边界明确的任务使用`opencode run '...'`（不需要pty）
3. 迭代任务使用`background=true, pty=true`启动`opencode`
4. 使用`process(action="poll"|"log")`监控长时间任务
5. 如果OpenCode需要输入，通过`process(action="submit", ...)`响应
6. 使用`process(action="write", data="\x03")`或`process(action="kill")`退出
7. 向用户总结文件变更、测试结果和后续步骤

## PR审查工作流

OpenCode内置PR命令：

```
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

或在临时克隆中隔离审查：

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run '审查此PR与main分支的差异，报告bug、安全风险、测试缺口和风格问题。' -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')", pty=true)
```

## 并行工作模式

使用独立工作目录/工作树避免冲突：

```
terminal(command="opencode run '修复#101问题并提交'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run '添加解析器回归测试并提交'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

## 会话与成本管理

列出历史会话：

```
terminal(command="opencode session list")
```

查看token使用量和成本：

```
terminal(command="opencode stats")
terminal(command="opencode stats --days 7 --models anthropic/claude-sonnet-4")
```

## 注意事项

* 交互式`opencode`(TUI)会话需要`pty=true`，`opencode run`命令不需要pty
* `/exit`不是有效命令 — 会打开代理选择器，使用Ctrl+C退出TUI
* PATH环境变量不匹配可能导致选择错误的OpenCode二进制/模型配置
* 如果OpenCode看起来卡住了，杀死进程前先查看日志：`process(action="log", session_id="<id>")`
* 避免在并行OpenCode会话之间共享同一个工作目录
* TUI中可能需要按两次Enter才能提交（第一次确认文本，第二次发送）

## 验证

冒烟测试：

```
terminal(command="opencode run '严格返回：OPENCODE_SMOKE_OK'")
```

成功标准：

* 输出包含`OPENCODE_SMOKE_OK`
* 命令退出无服务商/模型错误
* 编码任务：预期文件已更改且测试通过

## 使用规则

1. 一次性任务优先使用`opencode run` — 更简单，不需要pty
2. 仅当需要迭代时使用交互式后台模式
3. 始终将OpenCode会话限定在单个仓库/工作目录中
4. 长时间任务从`process`日志中提取进度更新告知用户
5. 报告具体的任务结果（更改的文件、测试情况、剩余风险）
6. 使用Ctrl+C或kill退出交互式会话，不要使用`/exit`
