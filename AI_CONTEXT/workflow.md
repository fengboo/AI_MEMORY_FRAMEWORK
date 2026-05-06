---
type: workflow
name: progressive_spec_workflow
scope: global
status: active
version: 0.2
last_updated: 2026-05-05
---

# 渐进式规格工作流（Progressive Specification Workflow）

## 何时启用

用于非 trivial 的 engineering、coding、RTL、circuit design、architecture、script automation、documentation、memory-system 和 skill-design 任务。

简单问题不要强制走完整流程。

## 必要产出

1. 需求理解（Requirement understanding）
2. 用户显式需求（Explicit user requirements）
3. AI 推断假设（AI-inferred assumptions）
4. 未决问题（Open questions）
5. 可默认项（Defaultable items）
6. 中间层规格（Intermediate spec）
7. 实现计划（Implementation plan）
8. 验证点（Validation points）

## 核心规则

不要把假设隐藏在实现选择里。

## 默认行为

如果某个假设风险较低，可以用合理默认值推进，但必须标记为 `[ASSUME]`。

## 用户 Review

只让用户 review 会影响 correctness、compatibility、architecture、verification、safety 或 future extensibility 的关键假设。低风险细节不需要逐条确认。

## 输出规范

- 解释和讨论用简洁的中文。
- code、API、interface、field、file name、tool name、domain term 保留英文。
- 涉及可信度判断时使用 `[FACT]` / `[INFER-H]` / `[INFER-L]` / `[ASSUME]` / `[UNKNOWN]` / `[OPINION]` 标注。
