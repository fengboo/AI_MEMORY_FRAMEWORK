# AI 协作工作流

对于非 trivial 的 engineering、coding、architecture、documentation 或 skill-design 任务，不要从自然语言需求直接跳到最终实现。

采用 progressive specification workflow（渐进式规格工作流）：

1. 理解需求。
2. 列出用户显式需求（explicit requirements）。
3. 列出 AI 推断假设（AI-inferred assumptions）。
4. 列出未决问题（open questions）。
5. 识别可暂时默认的低风险项（defaultable items）。
6. 生成中间层结构化规格（intermediate structured spec）。
7. 请用户 review 关键假设（material assumptions）。
8. 在已确认或已声明的默认值下推进实现。
9. 生成 tests、validation points 或 review checklist。
10. 保持 spec、code、test、documentation 对齐。

## 规则

- 不要把假设隐藏在实现选择里。
- 区分 fact、inference、assumption 和 uncertainty。
- 高风险或不确定的内容，提供 validation path。
- 把 AI 视为协作者（colleague），而非权威（authority）。
- 当检测到持久化 memory 冲突时，写入 `conflicts.md`，不要静默选择。
- 用户纠正 AI 时，生成 correction candidate，仅在用户确认后更新相关 memory。
- 能用真实 toolchain 验证的，就不要只做纸面验证。

## 上下文加载

读取 `AI_CONTEXT/README.md` 获取需要加载的文件列表。不要默认加载整棵文件树。

`README.md`（根目录）是给人类读的项目说明，不需要加载到 agent 上下文。
