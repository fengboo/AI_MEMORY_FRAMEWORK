---
id: python_sim_data_analysis
type: flow
scope: reusable
status: draft
domain:
  - analog_ic
  - simulation
  - data_analysis
tools:
  - python
  - pandas
  - numpy
  - matplotlib
used_by_projects: []
related_flows: []
related_tools:
  - python_analysis_stack
trust_level: medium
last_reviewed: 2026-05-26
last_updated: 2026-05-31
---

# Python Simulation Data Analysis Flow

## Purpose

用于分析仿真或测试数据，例如：

- Spectre transient / AC / PSS 导出的 CSV；
- ADC / DAC 指标提取；
- SerDes waveform；
- LDO stability / PSR / transient response；
- Monte Carlo / corner sweep 结果。

## Standard Flow

1. 明确输入数据格式；
2. 写 data loader；
3. 做 basic sanity check；
4. 提取关键 metrics；
5. 生成 plot；
6. 输出 summary report；
7. 保存脚本、输入路径、输出图和结论；
8. 如结果进入 memory，应记录 assumptions 和 validation status。

## Recommended Script Style

- 参数集中放在 `CONFIG` 或 CLI 参数；
- 不在脚本中硬编码过多绝对路径；
- 每个关键计算函数单独拆分；
- plot 需要有 title、axis label、unit；
- 输出目录可重复生成；
- 对异常数据给出 warning，而不是静默失败。

## Validation Checklist

- 输入文件是否存在；
- 数据列名是否符合预期；
- 单位是否一致；
- 是否处理 NaN / inf；
- 是否保存运行配置；
- 是否有至少一个 sanity plot；
- 关键 metric 是否可复现。

## When to Reuse

新项目只要涉及 Python 读取仿真/测试数据并提取指标，就可以引用本 flow。
