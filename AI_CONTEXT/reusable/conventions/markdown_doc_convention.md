---
id: markdown_doc_convention
type: convention
scope: reusable
status: draft
domain:
  - documentation
  - ai_memory
tools:
  - markdown
  - git
used_by_projects: []
related_flows: []
related_tools: []
trust_level: medium
last_reviewed: 2026-05-26
last_updated: 2026-05-31
---

# Markdown Documentation Convention

## Purpose

统一 AI_MEMORY_FRAMEWORK 中 Markdown 文档的写法，保证人类可读、AI 可检索、Git diff 清晰。

## Front Matter

建议所有长期 memory 文件包含 YAML front matter：

```yaml
---
id:
type:
scope:
status:
trust_level:
last_reviewed:
---
```

## Writing Style

- 中文描述为主；
- 英文 technical term 保留原文；
- 重要概念用稳定英文 id；
- assumption、decision、conflict、correction 明确分开；
- 不把未经确认的推测写成事实；
- 文件开头说明 purpose；
- 文件结尾可放 open questions / next steps。

## Section Template

```markdown
# Title

## Purpose

## Scope

## Key Rules / Decisions

## Assumptions

## Open Questions

## Related Files

## Change Log
```

## Git Diff Friendly Rules

- 避免一行写太长；
- 列表项保持一条一事；
- 不频繁重排无关内容；
- 大段自动生成内容应放在 generated 目录。
