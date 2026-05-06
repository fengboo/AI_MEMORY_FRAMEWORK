---
type: skill
name: engineering_spec_workflow
scope: global
status: active
version: 0.2
tags: [engineering, spec, coding, rtl, scripts, architecture]
last_updated: 2026-05-05
---

# Skill: 工程规格工作流

## 何时使用

用于非 trivial 的 engineering 任务、coding、RTL design、circuit design、scripts、architecture、documentation 和 skill design。

## 工作流

1. 需求理解（Requirement understanding）
2. 用户显式需求（Explicit user requirements）
3. AI 推断假设（AI-inferred assumptions）
4. 未决问题（Open questions）
5. 可默认项（Defaultable items）
6. 中间层结构化规格（Intermediate structured spec）
7. 实现计划（Implementation plan）
8. 验证点（Validation points）
9. 实现（Implementation）
10. 测试 / 验证 / review

## 硬规则

- 不要把假设隐藏在代码里。
- 非 trivial 任务不允许跳过 spec。
- 不要让用户 review 低风险细节。
- 必须让用户 review 关键假设（material assumptions）。
- 保持 spec、implementation、test、doc 对齐。
