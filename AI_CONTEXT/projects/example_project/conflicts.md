---
type: conflicts
scope: project/example_project
status: active
version: 0.1
last_updated: 2026-05-06
---

# 冲突记录

## CONFLICT-001: AI 回答风格偏好 — 同级冲突（示例）

- Status: resolved
- Detected: 2026-05-06
- Scope: global

### Statement A
- Source: user_preference
- Status: active
- Content: AI 回答应尽量简洁，避免冗长解释。

### Statement B
- Source: user_preference
- Status: active
- Content: AI 回答应尽量详尽，覆盖边界条件和潜在风险。

### Proposed resolution
两条 preference 来自不同场景。建议按场景分流：日常问答简洁，engineering / spec / review 详尽。

### User decision
- [x] Merge — 按场景分流
- [ ] Keep A
- [ ] Keep B
- [ ] Defer
- Resolution date: 2026-05-06

---

## CONFLICT-002: 技术选型偏好 — 不同级冲突（示例）

- Status: resolved
- Detected: 2026-05-06
- Scope: project/example_project

### Statement A
- Source: confirmed_decision
- Status: active
- Content: 项目检索以 Project Affinity 为主排序因子。

### Statement B
- Source: ai_assumption
- Status: deprecated
- Content: time decay 公式统一计算权重即可。

### Proposed resolution
Statement A 优先级更高。采用 Project Affinity 为主排序，time decay 仅作次级 soft heuristic。

### User decision
- [x] Merge（按 proposed resolution）
- [ ] Keep A
- [ ] Keep B
- [ ] Defer
- Resolution date: 2026-05-06

---

## 模板

### CONFLICT-YYYYMMDD-NNN: <主题>

- Status: pending
- Detected: YYYY-MM-DD
- Scope: project/xxx | global
- Statement A:
  - Source: user_confirmed | user_preference | ai_inferred | ai_default
  - Status: active | deprecated
  - Content:
- Statement B:
  - Source:
  - Status:
  - Content:
- Proposed resolution:
- User decision: [ ] Keep A  [ ] Keep B  [ ] Merge  [ ] Defer
- Resolution date:
