---
type: todo
scope: global
status: active
version: 0.1
last_updated: 2026-05-06
---

# TODO — AI Memory System

## Phase 0: Scaffolding

- [ ] Create `AGENTS.md` at repo root
- [ ] Create `AI_CONTEXT/` core files
- [ ] Create `AI_CONTEXT/projects/index.md`
- [ ] Create `AI_CONTEXT/skills/`
- [ ] Set up `scripts/` and `templates/`

## Phase 1: Memory Governance

- [ ] Write conflict examples to `conflicts.md`
- [ ] Write correction examples to `corrections.md`
- [ ] Test conflict exposure (agent must not silently choose)
- [ ] Test correction feedback loop
- [ ] Test trust label usage in engineering tasks
- [ ] Test progressive spec workflow

## Phase 2: Lightweight Retrieval

- [ ] Add aliases / triggers to `projects/index.md`
- [ ] Define retrieval fallback behavior
- [ ] Add `recent_active_project` concept
- [ ] Write health-check checklist

## Phase 3: Validation Loop

- [ ] Implement front matter lint script
- [ ] Implement link check script
- [ ] Define `validation_report.md` format
- [ ] Run first maintenance session

## Phase 4: Bridge & Pilot

- [ ] Harden bridge templates with read/write switches
- [ ] Select a pilot repo and install bridge
- [ ] Run real workflow tests (engineering task, fuzzy retrieval, correction)

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
