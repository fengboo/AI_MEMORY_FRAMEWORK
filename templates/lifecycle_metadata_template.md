# Lifecycle Metadata Template

> Future upgrade template. 当前不强制使用。

```yaml
---
id: example_memory_item
type: decision | assumption | conflict | correction | flow | tool | pattern | convention | route_log | raw_evidence | summary
scope: global | reusable | project | archive
lifecycle: active | warm | cold | archived | deprecated | superseded | deleted

importance: low | medium | high | critical
volatility: low | medium | high
reuse_count: 0

created_at:
last_accessed:
last_reviewed:
review_after:

source_projects: []
related_projects: []
related_tools: []
related_flows: []
tags: []

supersedes: []
superseded_by:

summary: ""

retrieval_policy:
  include_by_default: false
  include_when_tags_match: []
  exclude_when_archived: true
---
```

## Notes

- `lifecycle` controls whether this memory should be active, searchable, archived, or deprecated.
- `importance` is not the same as recency.
- `volatility` estimates how likely the memory is to become stale.
- `reuse_count` can support promotion from project memory to reusable memory.
- `superseded_by` prevents outdated memory from silently polluting new work.
- `retrieval_policy` is for future context routing.
