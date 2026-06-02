---
type: root_index
scope: global
status: active
version: 0.1
last_updated: 2026-05-06
---

# AI Context Root

本目录存储 AI agent 用到的可移植 memory、workflow 和 skill 上下文。

**人类读者**：请阅读仓库根目录的 `README.md`。本文档是给 AI agent 的加载路由指南。

## 始终相关（每次加载）

- `user_profile.md` — 用户偏好模板（使用前填写）
- `workflow.md` — 渐进式规格工作流定义与输出规范
- `constraints.md` — 项目约束（必须做 / 禁止做 / 推迟项）

## 可信度 / 验证

- `trust_policy.md` — 可信度标注规范（[FACT] / [INFER] / [ASSUME] / [UNKNOWN] / [OPINION]）
- `skills/trust_and_verification.md` — 可信度与验证 Skill 定义

## 工程 / coding / architecture / skill 设计

- `skills/engineering_spec_workflow.md` — 工程规格工作流 Skill

## Memory 治理

- `memory_policy.md` — memory 类型、优先级、Project Affinity、冲突/纠正规则、维护检查清单
- `projects/index.md` — 项目索引、活跃项目列表、触发词（Triggers）、检索规则
- `reusable/README.md` — 跨项目可复用 memory 的索引与提升规则

## 活跃项目

见 `projects/index.md`。

每个活跃项目下有：
- `index.md` — 项目总览
- `decisions.md` — 已确认决策
- `conflicts.md` — 冲突记录
- `corrections.md` — 纠正记录
- `open_questions.md` — 未决问题
- `route_log.md` — 检索路由日志
- `validation_plan.md` — 验证计划
- `supervision/` — 多角色协作通道

## 跨项目可复用 memory

`reusable/` 保存可跨项目复用的 memory，不替代 `projects/`。按需加载：

- `reusable/flows/` — 如何完成一类事情
- `reusable/tools/` — 工具用法、限制和常见坑
- `reusable/patterns/` — 抽象工程协作模式
- `reusable/conventions/` — 长期习惯和文档 / 代码约定

当某条项目经验被两个或以上项目复用，或预计未来会复用，可提升到 `reusable/`，再由项目 `index.md` 通过 `uses_flows`、`uses_tools`、`inherits_patterns`、`inherits_conventions` 等 metadata 引用。

## 全局 TODO

`TODO.md` — 包含 Phase 0-5 的完整任务列表与完成状态。

## 检索规则（加载顺序）

1. 当前活跃项目 > 其他项目。
2. 用户说"继续上次"、"之前那个"、"这个系统"或使用已知别名/触发词 → 匹配 `projects/index.md`。
3. `recent_active_project` 权重高于其他 active project。
4. 如果不确定匹配哪个项目，列出候选项目（candidate projects）而非猜测。
5. 无匹配时告知用户，询问是否创建新项目或直接回答。
6. 模糊请求的匹配结果写入对应项目的 `route_log.md`。
7. **不要默认加载整棵文件树。** 按需加载。
8. `reusable/` 也按需加载：只有任务匹配对应 flow / tool / pattern / convention 时才读取。
