---
type: policy
name: memory_governance
scope: global
status: active
version: 0.3
last_updated: 2026-05-05
---

# Memory 治理策略

## Memory 类型

- `confirmed_decision`：用户已确认的决策，最高优先级。
- `user_preference`：用户的稳定偏好。
- `ai_assumption`：AI 推断的假设，必须保持可覆盖（overrideable）。
- `temporary_assumption`：阶段性临时假设。
- `correction_candidate`：等待应用的用户纠正。
- `deprecated`：已失效，仅保留用于审计追溯。

## Memory 优先级

```
confirmed_decision (100)
  > user_preference (90)
  > project_decision (85)
  > ai_assumption (50)
  > temporary_assumption (20)
  > deprecated (0)
```

## Project Affinity

memory retrieval 以 Project Affinity 为主排序因子：

- `same_project`：高优先级 — 旧但同项目的 decision 权重高于新但不同项目的信息。
- `related_project`：中优先级。
- `same_domain`：低优先级。
- `unrelated`：最低优先级。

同项目内，以 `confirmed_decision > user_preference > ai_assumption` 排序。Time decay 仅作为同项目同优先级的次级 soft heuristic，不硬编码为强规则（DEC-005）。

## 更新规则

AI 可以提议 memory 更新，但关键 memory 的变更必须经过用户 review。

## 冲突规则

如果两条 memory 互相矛盾，写入对应项目的 `conflicts.md`。不要静默选择其中一条。

冲突裁决层级：
1. 用户明确确认的 decision
2. 用户长期 preference
3. 项目级 decision
4. AI high-confidence inference
5. AI default
6. 临时 assumption
7. deprecated / archive

## 纠正规则

用户纠正 AI 时：
1. 定位错误来源（memory / inference / outdated assumption / scope mismatch）
2. 标记原 memory 为 deprecated 或 corrected
3. 写入 `corrections.md` candidate
4. 更新相关 spec / decisions
5. 检查 cascading updates

## 轻量检索 v0

- 使用 `projects/index.md` 中的活跃项目列表。
- 使用项目 index 中的 aliases / triggers 做模糊匹配。
- `recent_active_project` 权重高于其他 active project。
- 如果不确定，列出候选项目（candidate projects）而非猜测。
- 模糊请求的匹配结果写入 `route_log.md`。

## 维护检查清单（Quick Health-Check）

每次项目阶段切换或连续多次工程任务结束时，检查以下项：

### Front matter 完整性
- [ ] 所有 `AI_CONTEXT/` 下 .md 文件有 `type` 字段
- [ ] key operational files 有 `status` 字段（active | deprecated）
- [ ] memory / decision 类文件有 `last_updated` 字段
- [ ] 无 `status: active` 但 `last_updated` 超过 60 天的文件（candidate for review）

### Index 引用完整性
- [ ] `projects/index.md` 中列出的项目文件均已存在
- [ ] `AI_CONTEXT/README.md` 引用的文件均已存在
- [ ] 各项目 `index.md` 的 Key Files 列表与实际文件一致

### 孤立文件检测
- [ ] 无未被任何 index 引用的 .md 文件（`reference/` 和 `supervision/` 除外）
- [ ] 无 `status: deprecated` 但仍被 active decision 引用的条目

### 冲突与纠正
- [ ] 无 `status: pending` 超过 30 天的 conflict
- [ ] 无 `status: candidate` 超过 30 天的 correction
- [ ] conflicts.md 中 resolved 条目占比 > pending

### Stale memory 检测
- [ ] 无 `temporary_assumption` 超过其声明有效期的文件
- [ ] 无 `ai_assumption` 与 `confirmed_decision` 矛盾且未写入 conflicts 的情况

满足上述检查的 ≥80% 即可视为健康。AI 可在检测到异常时建议用户做一次 maintenance session。

## Appendix: Future memory lifecycle design

当前 memory policy 主要覆盖 memory 可信度、冲突、纠正、轻量检索和项目级记录。

未来当 memory 数据规模增长后，可以追加 memory lifecycle 机制，用于控制：

- 哪些 memory 默认进入 AI context；
- 哪些 memory 只作为 archive / evidence；
- 哪些 route log 应被压缩为 summary；
- 哪些项目内经验应提升为 reusable flow / tool / pattern；
- 哪些旧决策应标记 deprecated 或 superseded；
- 哪些记忆需要 review。

当前不强制执行该机制，不要求现有 Markdown 文件补齐 lifecycle metadata，不改变 bridge 加载逻辑。

未来设计参考：

- `docs/future_memory_lifecycle_design.md`
- `docs/memory_lifecycle_policy_draft.md`
- `docs/future_upgrade_trigger_conditions.md`
