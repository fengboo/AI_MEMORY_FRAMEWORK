---
id: reusable_memory_root
type: index
scope: reusable
status: draft
trust_level: medium
last_reviewed: 2026-05-26
last_updated: 2026-05-31
---

# Reusable Memory

`reusable/` 用于保存跨项目可复用的 memory。

它不是替代 `projects/`，而是补充 project-based memory 的横向复用层。

## 子目录

```text
flows/        怎么做一类事情
tools/        某个工具怎么用、限制和坑
patterns/     抽象工程协作模式
conventions/  长期习惯和文档/代码约定
```

## 提升规则

当某条 memory 被两个或以上项目复用，或预计未来会复用，就应从 project memory 提升为 reusable memory，并由 project 通过 metadata 或 links 引用。

## Project 引用方式

项目 `index.md` 可以添加：

```yaml
uses_flows:
  - python_sim_data_analysis
uses_tools:
  - virtuoso_bridge
inherits_patterns:
  - spec_first_workflow
inherits_conventions:
  - markdown_doc_convention
```
