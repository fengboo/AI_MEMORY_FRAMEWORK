# 方法论概述

## 为什么需要这个系统

与 AI 协作做工程时，常见问题：

- AI 把假设藏在实现里，用户 review 成本高
- 每次新会话从零开始，之前确认的决策丢失
- 不同 AI 工具之间上下文无法迁移
- AI 的错误输出被当作事实接受
- memory 冲突时 AI 静默选一个

AI_MEMORY 解决这些问题的思路：**把 AI 协作从一次性问答变成可审查、可迁移、可迭代的工程系统。**

## 三层模型

```
自然语言需求（intent / context / uncertainty）
        ↓
中间层结构化规格（assumptions / questions / decisions）
        ↓
实现与验证（code / tests / toolchain）
```

自然语言擅长表达意图但不保证精确性。代码保证执行但不暴露假设。中间层负责把模糊需求以可审查的方式存在，随项目推进逐步收紧。

## 核心机制

### Progressive Spec Workflow
非 trivial 任务先输出 spec（需求理解 → 显式需求 → AI 假设 → 未决问题 → 可默认项 → 中间层规格），用户 review 后再实现。

### Memory Governance
- `decisions.md`：已确认的决策（canonical source of truth）
- `conflicts.md`：矛盾的 memory 落盘，不静默裁决
- `corrections.md`：用户纠正的闭环记录

### Trust Calibration
声明标注：`[FACT]` / `[INFER-H]` / `[INFER-L]` / `[ASSUME]` / `[UNKNOWN]` / `[OPINION]`。标注不证明正确性，但暴露声明类型，让用户知道哪些要 review。

### Bridge + Switches
工程项目通过 bridge 文件指向集中 AI_MEMORY。读/写开关控制每个项目的权限：
- 小项目：只读工作流
- 大项目：读写全开，经验积累

### Validation Loop
`scripts/ai_context_lint.py` 检查 front matter 完整性，`scripts/ai_context_link_check.py` 检查内部链接。验证原则：有工具闭环 > AI 自述 > 无验证。

## 不覆盖的范围

这个系统不替代：
- AI 产品自身的 memory 机制（ChatGPT Memory、Claude Projects 等）
- 向量数据库或 RAG pipeline
- Skill 编排引擎

它是**跨工具的 portable context layer**，配合现有 AI 工具使用，不是替代它们。
