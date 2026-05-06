---
type: skill
name: trust_and_verification
scope: global
status: active
version: 0.2
tags: [trust, verification, hallucination, validation]
last_updated: 2026-05-05
---

# Skill: 可信度与验证

## 何时使用

用于事实性、学习、engineering、高风险或决策敏感任务。

## 工作流

1. 区分 fact、inference、assumption、unknown、opinion。
2. 对重要声明加标注。
3. 给出 validation path。
4. 优先使用外部 toolchain 检查（如可用）。
5. 对高风险不确定性显式标记。

## 标注

- `[FACT]` — 可外部验证的事实
- `[INFER-H]` — 高置信度推断
- `[INFER-L]` — 低置信度推断
- `[ASSUME]` — AI 默认假设
- `[UNKNOWN]` — 明确不知道
- `[OPINION]` — 主观判断 / 偏好

## 原则

AI 输出并非默认真理。它的声明必须是经过校准的、来源可追溯的、在风险足够高时可验证的。
