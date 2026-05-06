---
type: project_index
scope: global
status: active
version: 0.1
last_updated: 2026-05-06
---

# 项目索引

## 活跃项目

| 项目 | 路径 | 状态 | 别名（Aliases） | 触发词（Triggers） |
|---|---|---|---|---|
| Example Project | `projects/example_project/` | active | demo, example, sample project | 继续上次, 之前那个, example |

## 最近活跃项目

| 项目 | 最后活跃 | 会话 |
|---|---|---|
| Example Project | 2026-05-06 | demo session |

## 检索规则

1. 优先匹配 active project。
2. `recent_active_project` 权重高于其他 active project。
3. 多候选时列出而非猜测。
4. 无匹配时告知用户，询问是否创建新项目或直接回答。
5. 模糊请求的匹配结果写入对应项目的 `route_log.md`。

## 如何添加新项目

1. 在 `projects/` 下创建 `<project_name>/` 目录。
2. 在此表添加一行，指定 aliases / triggers。
3. 在项目目录中创建 `index.md`、`decisions.md`、`open_questions.md`、`conflicts.md`、`corrections.md`、`route_log.md`、`validation_plan.md`。
4. 可选：创建 `supervision/` 用于多角色协作。
