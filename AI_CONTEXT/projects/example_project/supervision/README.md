---
type: supervision_index
scope: project/example_project
status: active
version: 0.1
last_updated: 2026-05-06
---

# Supervision Channel

本目录用于用户、监工 AI、执行 AI 之间的项目级协作。

## 角色分工

- 用户：最终裁决关键方向、冲突、memory 更新和验收标准。
- 监工 AI：把握项目方向，在大节点 review，不干预执行 AI 的日常细节。
- 执行 AI：按 `EXECUTOR_BRIEF.md` 推进实现、测试和记录，遇到 blocker 时写入 `QUESTIONS.md`。

## 使用规则

- 日常实现细节不要写进本目录，除非它影响方向、验收、风险或需要用户裁决。
- 执行 AI 完成 checkpoint 后，在 `HANDOFF_LOG.md` 写简短交接摘要。
- 有疑问先写入 `QUESTIONS.md`，标明是否 blocker。
- 监工 AI 做阶段 review 时，以 `REVIEW_CHECKPOINTS.md` 为准。
