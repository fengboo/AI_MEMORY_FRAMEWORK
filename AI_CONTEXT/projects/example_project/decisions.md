---
type: decisions
scope: project/example_project
status: active
version: 0.1
last_updated: 2026-06-17
---

# 项目决策

## DEC-001: 使用 AI_MEMORY 管理项目上下文（示例）

Status: confirmed

理由：Markdown 文件树可读、可编辑、可 diff、Git 友好，可跨 AI 工具移植。

## DEC-002: 不在 Phase 1 构建完整 memory OS（示例）

Status: confirmed

理由：先跑通最小治理闭环——conflicts、corrections、trust labels、workflow。

## DEC-003: Bridge root path 默认通过 `AI_MEMORY_ROOT` 环境变量解析（示例）

Status: confirmed

理由：AI_MEMORY 是集中式 memory repo，但不同平台、不同机器上的绝对路径不同。bridge 文件应默认使用 `${AI_MEMORY_ROOT}` 等环境变量引用，让其他工程项目不需要写入平台相关绝对路径。若某个 AI 工具无法读取环境变量，允许在该项目 bridge 中临时覆盖为显式绝对路径。

## DEC-004: Bridge install 必须合并已有 agent 文件而非覆盖（示例）

Status: confirmed

理由：许多工程项目已经有本地 `AGENTS.md` 或 `CLAUDE.md`，这些文件可能包含项目特定规则。安装 AI_MEMORY bridge 时必须保留原内容，将 bridge 内容合入独立的 `AI_MEMORY Bridge` section；若发现 material conflict，应报告给用户而不是静默覆盖或裁决。

## 如何添加真实决策

1. 使用 `DEC-NNN` 编号。
2. 标注 Status：confirmed / proposed / deprecated。
3. 写下理由（Rationale）。
4. 用户确认后从 proposed 改为 confirmed。
