# Future Memory Lifecycle Design

## 1. 问题来源

AI_MEMORY_FRAMEWORK 的当前结构基于 Markdown 文件树，适合早期项目积累、人工审查、跨工具迁移和 AI 读取。

随着项目维护时间增长，会出现以下问题：

1. `projects/` 数量增长，历史项目越来越多。
2. `route_log.md` 和讨论记录膨胀。
3. 相似经验在多个项目里重复出现。
4. 旧决策可能被新决策替代，但仍留在 active context。
5. 工具经验、流程经验、用户习惯散落在项目目录中。
6. AI 检索时可能读取过多低价值或过期信息。
7. 人类查看时也会被信息量淹没。

因此，长期 memory system 不能只依赖“持续追加”。

需要引入：

```text
memory lifecycle
memory compression
archive tier
deprecation / superseding
retrieval policy
memory health dashboard
```

## 2. 设计原则

### 2.1 长期保存不等于长期激活

某些历史记录需要保留以便追溯，但不应默认参与 AI context。

```text
preserved ≠ active
archived ≠ deleted
compressed ≠ lost
forgotten ≠ destroyed
```

### 2.2 类人遗忘不是简单删除

人类记忆中的“遗忘”更像：

- 细节淡化；
- 高频经验抽象成模式；
- 低频记忆不主动浮现；
- 强线索触发时可以追溯；
- 错误认知被修正或降权；
- 重复经验变成习惯或原则。

对应 AI_MEMORY：

```text
raw logs → phase summary → project summary → reusable pattern → global convention
```

### 2.3 先记录想法，后实现机制

当前数据还少，完整 lifecycle 系统不迫切。

当前只需要：

- 写清未来设计；
- 预留 metadata；
- 定义触发条件；
- 保持现有 architecture 不变。

未来当数据规模足够后再合入。

## 3. 建议的未来 memory tiers

```text
Tier 0: Runtime Context
当前任务临时上下文，不长期保存，或只保存摘要。

Tier 1: Active Memory
当前项目、高频 reusable flow、用户长期偏好、正在使用的决策。

Tier 2: Consolidated Memory
经过整理、去重、抽象后的稳定知识，例如 lessons learned、recurring patterns。

Tier 3: Archive Memory
历史项目、旧 route log、完整讨论记录、低频资料。默认不进入 AI context。

Tier 4: Raw Evidence
原始对话、原始日志、原始实验记录、旧版本文件。仅用于审计和追溯。
```

## 4. 未来可能的目录结构

当前不建议马上创建这些目录。未来升级时可加入：

```text
AI_CONTEXT/
├── reusable/
├── projects/
├── consolidated/
│   ├── project_summaries/
│   ├── lessons_learned.md
│   └── recurring_patterns.md
├── archive/
│   ├── projects/
│   ├── raw_logs/
│   ├── deprecated/
│   └── superseded/
└── index/
    ├── context_routing.md
    ├── active_index.md
    ├── archive_index.md
    └── memory_health.md
```

## 5. Memory lifecycle states

未来可以定义以下状态：

```text
active       默认可进入 AI context
warm         可检索，但不默认加载
cold         低频，仅相关性强时加载
archived     归档，只在追溯/审计/明确要求时读取
deprecated   不再推荐使用，但保留原因
superseded   已被新文件替代
deleted      明确删除或不再保留
```

## 6. Memory processing pipeline

```text
Capture → Classify → Consolidate → Promote → Archive → Prune
```

### Capture

先记录在项目层，例如：

```text
projects/active/project_x/route_log.md
projects/active/project_x/decisions.md
```

### Classify

判断 memory 类型：

- project-specific decision
- reusable flow
- tool usage
- user preference
- temporary note
- raw evidence
- correction
- conflict

### Consolidate

把原始记录压缩成 summary。

例如：

```text
20 条 route_log
↓
phase_summary.md
```

### Promote

如果某条经验跨项目复用，提升为 reusable memory。

```text
projects/project_x/notes.md
↓
reusable/flows/python_sim_data_analysis.md
```

### Archive

旧项目、低频日志、已被总结过的细节移入 archive。

### Prune

错误、重复、过时内容标记 deprecated 或 superseded。

不建议早期物理删除；优先 deprecated / archived。

## 7. 类遗忘规则示例

未来可以采用简单规则，不必一开始上复杂算法：

```text
Rule A: 项目 route_log 在阶段结束后压缩为 phase summary。
Rule B: 某经验被 2 个项目用到，标记 reusable_candidate。
Rule C: 某经验被 3 个项目用到，提升为 reusable memory。
Rule D: active memory 90 天未使用，进入 review queue。
Rule E: active memory 180 天未使用且已有 summary，降级为 archive。
Rule F: superseded memory 默认不参与检索。
Rule G: route_log 默认不进入 active context，只作为 evidence。
```

## 8. Retrieval policy

未来 AI 不应每次读全库，而应按任务构造 context pack：

```text
Step 1: 读取 active_index.md
Step 2: 根据任务 tags 找 reusable memory
Step 3: 读取当前 project 的 project.md / decisions.md
Step 4: 只有必要时查 archive_index.md
Step 5: archive/raw logs 默认不读
```

## 9. Memory health dashboard

未来 `site/` viewer 可以加入：

```text
memory_health.html
review_queue.html
archive_candidates.html
promote_candidates.html
deprecated.html
```

显示：

```text
Active memories
Warm memories
Archived memories
Deprecated memories
Pending review
Stale active memories
Duplicate candidates
Promote candidates
Archive candidates
```

## 10. 当前阶段结论

当前不实现完整 lifecycle 机制。

只做：

1. 记录本文档。
2. 可选预留 metadata 模板。
3. 在 README / memory_policy 中注明 future upgrade。
4. 等数据规模扩大后再合入。

这避免 premature over-engineering，同时保留未来扩展路径。
