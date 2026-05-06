---
type: constraints
scope: project
status: active
version: 0.1
last_updated: 2026-05-05
---

# 项目约束

## 首要原则

构建最小化、可审查的 AI context 系统。不要在 Phase 0/1 构建完整的 memory OS。

## 必须做

- 以 Markdown 文件作为 canonical memory 载体。
- 关键文件使用 YAML front matter。
- 用户确认的决策与 AI 假设分离存储。
- 冲突写入 `conflicts.md`。
- 用户纠正以 candidate 形式写入 `corrections.md`。
- 操作文件与参考文档分离存储。
- 倾向于小步、可审查的变更。
- memory 更新时生成 diff 或显式变更摘要。

## 禁止做

- 不静默覆盖已确认的 memory。
- 不在用户 review 前自动裁决关键冲突。
- 不默认加载整棵 memory tree。
- 不将 AI confidence 当作 ground truth。
- 不在轻量 routing 层可用之前引入 vector retrieval。
- 不在第一阶段对每个 skill 强行 schema 化。

## 推迟项

- Vector retrieval / RAG
- Cross-model conformance test suite
- Full Skill JSON Schema I/O
- Complex Skill orchestration
- Automated memory rewriting
- Multi-agent delegation framework
