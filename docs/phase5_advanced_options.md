# Phase 5 — Advanced Options

以下特性不在当前框架中实现，但作为未来扩展方向记录。

## Skill JSON Schema I/O

把 skill 的输入、输出、适用条件、validation contract 结构化。

- `preconditions`：skill 启动前必须满足的条件
- `postconditions`：skill 完成后的可检查保证
- `failure_modes`：已知失败模式和处理策略
- `json_schema`：输入/输出的结构化定义

适合场景：需要 sub-agent 编排或多 skill 串联时。

## Skill Composition / Orchestration

定义 spec workflow → implementation → validation → correction capture 等 skill 串联逻辑。

适合场景：复杂工程 pipeline 需要多个 skill 按序执行。

## Sub-agent Context Packages

给子 agent 分发 least-privilege context package，避免整棵 memory tree 暴露。

- 只包含 task brief + relevant spec + I/O format + constraints + examples
- 不包含无关项目 memory、deprecated 条目、全局 user profile

适合场景：用弱模型执行子任务时防止上下文污染。

## Cross-model Conformance Test Suite

测试不同 AI 工具（Codex / Claude / Cursor / DeepSeek 等）是否遵守同一 memory policy。

- 给定相同的 `AI_CONTEXT/`，不同模型的行为是否一致
- 测试项目：conflict detection、correction flow、trust label usage、progressive spec adherence

注意：文件树迁移的是 identity/规则，迁移不了 reasoning capability。测试的是最低行为约束，不是完全一致性。

## Vector Retrieval / RAG

为大规模 memory（10+ 项目、100+ memory 条目）增加 embedding / vector index。

- 当前 lightweight retrieval（index + aliases + triggers + route_log）适合小规模
- 当项目数增长时，语义检索可提高命中率

注意：先让 lightweight routing 层可用，再加 vector retrieval。

## Session-to-memory Bridge

把会话摘要转成可 review 的 memory candidate。

- AI 在会话结束时生成摘要
- 用户 review → accepted → 写入 `decisions.md` 或更新相关 memory
- 用户 reject → 丢弃或标记为 temporary

注意：依赖会话摘要质量和 retrieval 准确性。

## Automated Memory Rewriting

自动维护 decisions / corrections / conflicts。

风险最高，一律 deferred。需要：
- 冲突检测达到高准确率
- 用户信任 automated maintenance
- cascading update 逻辑完善

在此之前，memory 更新始终需要用户 review。
