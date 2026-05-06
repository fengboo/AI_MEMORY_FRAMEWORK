---
type: corrections
scope: project/example_project
status: active
version: 0.1
last_updated: 2026-05-06
---

# 纠正记录

## CORRECTION-001: AI 对 API 版本的错误声明 — factual_error（示例）

- Status: synthetic（示例，非真实用户纠正）
- 用户纠正内容: "不对。Python 3.12 没有移除 GIL。PEP 703 推迟到 3.13+。"
- AI 原始声明: "[FACT] Python 3.12 移除了 GIL。"
- 错误类型: factual_error
- 受影响文件: 相关性能优化建议的记录
- 建议更新: 更正声明，检查是否有其他文件引用了错误前提
- 用户决定: [ ] 确认应用更新  [ ] 仅记录，暂不修改

---

## CORRECTION-002: 用户纠正 AI 的项目状态假设（示例）

- Status: synthetic（示例，非真实用户纠正）
- 用户纠正内容: "项目已从原型阶段进入正式开发，核心模块改用 Rust。"
- AI 原始声明: "[ASSUME] 项目当前处于 Python 快速验证阶段。"
- 错误类型: outdated_assumption
- 受影响文件: 语言选择、性能预算相关假设
- 建议更新: 标记旧 assumption 为 deprecated，新增 confirmed_decision
- 用户决定: [ ] 确认应用更新  [ ] 仅记录，暂不修改

---

## 模板

### CORRECTION-YYYYMMDD-NNN: <主题>

- Status: candidate
- 用户纠正内容:
- AI 原始声明:
- 错误类型: factual_error | outdated_assumption | scope_mismatch | overconfident_inference | retrieval_error
- 受影响文件:
- 建议更新:
- 用户决定:
