---
type: executor_brief
scope: project/example_project
status: active
version: 0.1
last_updated: 2026-05-06
---

# Executor Brief

## 当前任务

按 `TODO.md` 推进当前 Phase。遇到 blocker 写入 `QUESTIONS.md`。

## 做事边界

- 不静默改写 confirmed memory
- 用户纠正先进入 `corrections.md` candidate
- 同级冲突必须暴露给用户
- 不默认加载整棵 `AI_CONTEXT/`

## 产出要求

每完成一个 checkpoint 在 `HANDOFF_LOG.md` 写一条摘要。
