---
type: policy
name: trust_and_verification_policy
scope: global
status: active
version: 0.2
last_updated: 2026-05-05
---

# 可信度与验证策略

## 声明标注

在 engineering、学习、事实性、高风险或决策敏感任务中使用以下标注：

| 标注 | 含义 | 用户行动 |
|---|---|---|
| `[FACT]` | 可外部验证的事实 | 可选验证 |
| `[INFER-H]` | 高置信度推断 | 快速确认 |
| `[INFER-L]` | 低置信度推断 | 必须 review |
| `[ASSUME]` | AI 默认假设 | 关键假设必须 review |
| `[UNKNOWN]` | 明确不知道 | 需要补充信息或调研 |
| `[OPINION]` | 主观判断 / 偏好 | 用户决定 |

## 核心规则

- 标注不代表证明正确性，它暴露的是声明的类型。
- 高风险或时效敏感的事实，应使用外部来源验证。
- code、RTL、script 优先使用真实 toolchain 验证。
- 学习类回答应说明边界条件和常见误区。
- 把 AI 输出视为校准过的参考，而非默认真理。
