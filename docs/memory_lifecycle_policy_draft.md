# Memory Lifecycle Policy Draft

> 状态：Draft / Future Upgrade
>
> 当前不强制执行。未来当 memory 数据规模增长后，可升级为正式 policy。

## 1. Policy statement

AI_MEMORY_FRAMEWORK does not treat all memories as permanently active.

Each memory item may eventually have:

- lifecycle state
- importance
- volatility
- review schedule
- source projects
- supersession relation
- retrieval policy

Archive memory is preserved for traceability but excluded from default AI context.

## 2. Memory classes

```text
preference       用户长期偏好
decision         决策
assumption       假设
conflict         冲突
correction       纠正
flow             可复用流程
tool             工具经验
pattern          工程模式
convention       写作/代码/协作约定
route_log        执行日志
raw_evidence     原始证据
summary          压缩摘要
```

## 3. Lifecycle states

```text
active
warm
cold
archived
deprecated
superseded
deleted
```

## 4. Suggested default retention behavior

| Memory class | Default lifecycle | Review cadence | Notes |
|---|---:|---:|---|
| preference | active | long | 用户长期偏好，除非用户修改 |
| global decision | active | medium/long | 影响多个项目 |
| project decision | active/warm | project phase | 项目结束后可总结 |
| reusable flow | active | medium | 跨项目复用 |
| tool note | warm | short/medium | 工具可能变化 |
| route_log | warm/cold | short | 阶段结束后压缩 |
| raw evidence | archived | on demand | 默认不进入 context |
| deprecated note | deprecated | on demand | 仅用于追溯 |
| superseded note | superseded | on demand | 指向 replacement |

## 5. Suggested lifecycle metadata

```yaml
---
id: example_memory_item
type: flow
scope: reusable
lifecycle: active

importance: medium
volatility: medium
reuse_count: 0

created_at:
last_accessed:
last_reviewed:
review_after:

source_projects: []
related_projects: []
related_tools: []
related_flows: []

supersedes: []
superseded_by:

summary: ""

retrieval_policy:
  include_by_default: false
  include_when_tags_match: []
  exclude_when_archived: true
---
```

## 6. Review queue rules

Future scripts may add items to review queue when:

- active memory is stale;
- memory has no summary;
- duplicated content is detected;
- deprecated/superseded relation is missing;
- route_log is long but no phase summary exists;
- memory is referenced by many projects and should be promoted to reusable;
- reusable memory has not been reviewed after tool/API changes.

## 7. Non-goals for current phase

- No database.
- No vector DB.
- No automatic deletion.
- No mandatory lifecycle fields for all existing Markdown files.
- No automatic migration of project directories.
- No change to current bridge read/write switches.
