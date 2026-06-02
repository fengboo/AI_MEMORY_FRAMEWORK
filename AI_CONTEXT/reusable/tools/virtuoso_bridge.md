---
id: virtuoso_bridge
type: tool
scope: reusable
status: draft
domain:
  - analog_ic
  - eda
  - cadence
tools:
  - cadence_virtuoso
  - skill
used_by_projects: []
related_flows:
  - cdl_hierarchy_extraction
related_tools:
  - cadence_virtuoso
trust_level: medium
last_reviewed: 2026-05-26
last_updated: 2026-05-31
---

# Virtuoso Bridge Tool Memory

## Purpose

记录通过 bridge / API / 脚本方式调用 Cadence Virtuoso 的通用经验。

适用场景：

- AI 辅助生成 schematic；
- CDL / netlist 转 schematic；
- 自动创建 symbol；
- 批量调整 instance placement；
- 读取或写入 cellview；
- 生成 testbench；
- 执行 SKILL / Python bridge automation。

## Key Principles

1. GUI 可读性和 netlist 正确性是两套目标；
2. schematic 生成不能只保证连接正确，还要考虑人类可读布局；
3. diff pair、current mirror、cascode、load、bias 等 analog primitive 应尽量按语义分组；
4. power 在上、ground 在下、signal left-to-right 是默认可读性 convention；
5. bridge 操作应尽量可重放、可验证；
6. 关键修改应输出 log 和 summary。

## Common Risks

- GUI 状态依赖；
- API 覆盖不完整；
- cellview lock / library path 问题；
- symbol pin order 与 schematic 不一致；
- 仅 netlist 正确但 schematic 难以阅读；
- PDK callback 参数和显示参数不一致；
- 大型设计中操作速度较慢。

## Recommended Validation

- 打开目标 cellview；
- 检查 instance count；
- 检查 pin list；
- 检查 subckt / symbol 对应关系；
- 运行 netlist；
- 比较生成 netlist 与原始 netlist；
- 对关键 block 人工 review schematic readability。

## Related Flows

- CDL hierarchy extraction；
- CDL to schematic；
- analog primitive recognition；
- schematic readability cleanup。
