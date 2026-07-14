---
type: todo
scope: global
status: active
version: 0.1
last_updated: 2026-05-06
---

# TODO — AI Memory System

## Phase 0: Scaffolding（implemented）

- [x] Root `AGENTS.md`、`AI_CONTEXT/` core files、project index、skills、scripts 与 templates 已存在。

## Phase 1: Memory Governance（implemented examples）

- [x] `example_project/conflicts.md` 包含不同优先级的 conflict examples。
- [x] `example_project/corrections.md` 包含 correction examples。
- [ ] 真实跨模型行为验证仍待后续 conformance work；示例不等于真实验证。

## Phase 2: Lightweight Retrieval（implemented）

- [x] `projects/index.md` 包含 aliases、triggers、recent active project 与 fallback behavior。
- [x] `memory_policy.md` 包含 health-check checklist。

## Phase 3: Validation Loop（implemented and regression-tested）

- [x] Front matter lint、link check、bridge config check 与 site builder 已实现。
- [x] `tests/test_diagnostics.py` 覆盖 lint stale warning 与 bridge info 的 exit semantics。
- [x] `.github/workflows/validate.yml` 运行 tests、validators 与 site build。
- [ ] 首次真实 maintenance session 保留为使用者项目的后续工作。

## Phase 4: Bridge & Pilot（bridge hardening implemented）

- [x] 统一 `AGENTS.bridge.md` + `CLAUDE.md -> AGENTS.md` symlink 方案。
- [x] Bridge install guide 定义 merge-preserving workflow 与 `AI_MEMORY_ROOT`。
- [ ] 真实项目 pilot 与 real workflow tests 不在公共示例库内宣称完成。

## Phase 5: Advanced（Deferred）

以下特性推迟到未来评估：

- Skill JSON Schema I/O
- Skill composition / orchestration
- Sub-agent context packages
- Cross-model conformance test suite
- Vector retrieval / RAG
- Session-to-memory bridge
- Automated memory rewriting

详见 `docs/phase5_advanced_options.md`。
