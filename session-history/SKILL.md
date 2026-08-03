---
name: session-history
description: "检索 opencode 历史会话（含已归档），支持关键词搜索、状态筛选、时间范围过滤、模型过滤、消息详情查看。"
---

# Session History 历史会话检索

直接查询 opencode 本地 SQLite 数据库，检索历史会话记录及消息内容。

## 数据库路径

默认：`~/.local/share/opencode/opencode.db`（自动适配当前用户 home 目录）

可通过环境变量 `OPENCODE_DB` 覆盖。

## 快速使用

```powershell
# 搜索会话
python <skill_dir>/search_sessions.py [关键词] [active|archived|all] [模型关键词] [起始日期] [截止日期]

# 查看会话详情
python <skill_dir>/view_session.py <session_id>

# 统计信息
python <skill_dir>/stats.py
```

完整文档（中英双语）：[GitHub](https://github.com/q1023884985/opencode-session-history)

## 注意事项

- 写操作前建议关闭 opencode 桌面版，避免数据库锁
- `time_created` / `time_archived` 为 Unix 毫秒时间戳
- `model` 字段是 JSON 字符串，需 `json.loads()` 解析后取 `id`
