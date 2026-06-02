# Future Upgrade Trigger Conditions

> 目的：避免过早工程化。
>
> Memory lifecycle / archive / forgetting 机制只有在数据规模和噪声问题真实出现时才合入。

## Recommended trigger conditions

满足任意 2 条，可以开始 Phase Future 设计实现：

1. `AI_CONTEXT/projects/` 下项目总数超过 10 个。
2. active 项目超过 5 个。
3. `AI_CONTEXT/reusable/` 下 flow/tool/pattern/convention 总数超过 30 个。
4. 单个项目的 `route_log.md` 超过 1000 行或 50KB。
5. AI 在任务中频繁引用过期决策或旧工具方法。
6. 同一经验在 3 个及以上项目中重复出现。
7. 人类 review 时明显感觉 project notes / route_log 噪声太大。
8. site viewer 中需要 stale / duplicate / pending review / archive candidates 页面。
9. AGENTS bridge 或 Codex handoff 中需要显式 context selection，而不是加载固定文件。
10. 用户开始需要历史追溯、审计和“为什么当时这么决定”的独立查询路径。

## Phase Future minimal implementation

真正开始实现时，也应分阶段：

### Future-1: Metadata only

- 在模板中加入 lifecycle metadata。
- 不迁移历史文件。
- 加 `memory_health.py` 只读检查。

### Future-2: Health dashboard

- `memory_health.py` 输出 `site/generated/memory_health.html` 或 `.json`。
- 列出 stale / duplicate / archive candidates。
- 不自动修改文件。

### Future-3: Consolidation workflow

- 新增 `consolidate_project.py`。
- 由 AI 生成 proposed summary。
- 用户 review 后合入。

### Future-4: Archive workflow

- 新增 `archive_stale_memory.py`。
- 默认 dry-run。
- 只生成 proposed moves，不自动移动。

### Future-5: Retrieval routing

- 新增 `retrieve_context.py`。
- 根据任务描述、tags、当前项目生成 context pack。
- archive 默认不进入 context。

## Stop condition

如果 lifecycle 机制本身开始变成主要维护负担，应暂停，并回到更简单的规则：

```text
keep active small
archive raw logs manually
promote repeated flows manually
```
