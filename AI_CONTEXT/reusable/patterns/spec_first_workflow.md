---
id: spec_first_workflow
type: pattern
scope: reusable
status: active
domain:
  - ai_collaboration
  - engineering
tools:
  - codex
  - chatgpt
  - claude_code
used_by_projects: []
related_flows:
  - codex_handoff_pack
related_tools: []
trust_level: high
last_reviewed: 2026-05-26
last_updated: 2026-05-31
---

# Spec-first Workflow

## Purpose

把自然语言需求逐步转化为可实现、可验证、可审查的工程任务。

核心流程：

```text
自然语言讨论
    ↓
结构化 spec
    ↓
assumptions / open questions
    ↓
实现计划
    ↓
代码 / 文档 / 脚本
    ↓
验证
    ↓
memory update
```

## Rules

1. AI 必须显式列出 assumptions；
2. 关键假设需要用户 review；
3. 不确定信息不能静默固化为长期 memory；
4. 用户纠正应进入 corrections candidate；
5. 冲突信息进入 conflicts，不由 AI 静默裁决；
6. 实现后应保留 handoff log。

## When to Use

- 长期工程项目；
- Codex / Claude Code 执行任务；
- 需要 AI 记住偏好和流程；
- 多轮讨论后要交给执行 agent 落地；
- 项目有明显设计决策和放弃方案。
