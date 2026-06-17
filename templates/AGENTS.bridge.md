---
type: template
name: agents_bridge
scope: global
version: 0.4
description: 放在任何工程目录根下，作为通向 AI_MEMORY 集中上下文的桥梁
---

<!-- AI_MEMORY_ROOT = ${AI_MEMORY_ROOT} -->
<!-- 推荐先在系统/用户环境变量中设置 AI_MEMORY_ROOT。
     如果当前 AI 工具无法读取环境变量，可将上一行改为显式绝对路径。 -->

<!-- 通常只需要调整本文件顶部的 Bridge Switches。
     只有需要项目级覆盖时，才修改 AI_MEMORY_ROOT。
     下方正文只是说明，不作为第二份配置。 -->

<!-- ============================================================
     Bridge Switches — 按项目需求调整 (on / off)
     ============================================================

     预设组合：
       小项目 / 临时任务：仅 GLOBAL_WORKFLOW_RO = on，其余全部 off
       中型项目：         GLOBAL_WORKFLOW_RO + SKILLS_RO = on，PROJECT_MEMORY_RO = on，只读不写
       大项目 / 长期：    全部 on（读写全开，经验积累）

     ============================================================ -->

<!-- 读开关：控制 agent 从 AI_MEMORY 加载哪些内容 -->
<!-- GLOBAL_WORKFLOW_RO  = on -->   <!-- user_profile, workflow, constraints（每次必加载） -->
<!-- MEMORY_POLICY_RO    = off -->  <!-- memory_policy, trust_policy（冲突/纠正/可信度规则） -->
<!-- PROJECT_MEMORY_RO   = off -->  <!-- 项目级 decisions, conflicts, corrections, open_questions -->
<!-- SKILLS_RO           = on -->   <!-- engineering_spec_workflow, trust_and_verification skills -->

<!-- 写开关：控制 agent 能否向 AI_MEMORY 写入（仅在依赖读开关为 on 时生效） -->
<!-- PROJECT_MEMORY_RW   = off -->  <!-- 写入 decisions / conflicts / corrections -->
<!-- ROUTE_LOG_RW        = off -->  <!-- 写入 route_log（检索命中记录） -->

# 项目协作规则

## Bridge Switches 说明

本文件顶部的 `Bridge Switches` 是唯一 authoritative config。需要改读写权限时，只改顶部注释块中的 `on / off`，不要改正文说明。

`AI_MEMORY_ROOT` 是 AI_MEMORY 集中仓库的位置。推荐在每台机器上设置一次系统/用户环境变量，然后所有项目的 bridge 都保持：

```text
AI_MEMORY_ROOT = ${AI_MEMORY_ROOT}
```

Agent 解析路径时先展开该变量，再读取 `{AI_MEMORY_ROOT}/AI_CONTEXT/...`。支持的变量写法：

- `${AI_MEMORY_ROOT}`
- `$AI_MEMORY_ROOT`
- `%AI_MEMORY_ROOT%`
- `env:AI_MEMORY_ROOT`

如果环境变量不可用，agent 应要求用户提供路径，或仅输出 proposed diff / suggested update，不应猜测 AI_MEMORY 位置。

**读开关：**
| 开关 | 控制内容 | 建议 |
|---|---|---|
| `GLOBAL_WORKFLOW_RO` | user_profile, workflow, constraints | 始终 on |
| `MEMORY_POLICY_RO` | memory_policy, trust_policy | 需要冲突/纠正机制时 on |
| `PROJECT_MEMORY_RO` | 项目级 decisions, conflicts, corrections, open_questions | 长期项目 on |
| `SKILLS_RO` | engineering_spec_workflow, trust_and_verification skills | 工程任务 on |

**写开关：**
| 开关 | 控制内容 | 依赖 |
|---|---|---|
| `PROJECT_MEMORY_RW` | 写入 decisions / conflicts / corrections | `PROJECT_MEMORY_RO = on` 且 `MEMORY_POLICY_RO = on` |
| `ROUTE_LOG_RW` | 写入 route_log | `PROJECT_MEMORY_RO = on` |

**典型场景（示例组合，不是当前配置）：**
```
# 小项目 / 临时问个问题 → 只有 workflow，不碰记忆
GLOBAL_WORKFLOW_RO = on, 其余 off

# 中型项目 → 读项目记忆，只读不写
GLOBAL_WORKFLOW_RO = on, PROJECT_MEMORY_RO = on, SKILLS_RO = on

# 大项目 / 长期 → 全开，经验积累
全部 on
```

---

## 全局上下文

以下加载行为由顶部 switches 控制。

### 当 `GLOBAL_WORKFLOW_RO` 为 on

1. `{AI_MEMORY_ROOT}/AI_CONTEXT/user_profile.md`
2. `{AI_MEMORY_ROOT}/AI_CONTEXT/workflow.md`
3. `{AI_MEMORY_ROOT}/AI_CONTEXT/constraints.md`

### 当 `MEMORY_POLICY_RO` 为 on

- `{AI_MEMORY_ROOT}/AI_CONTEXT/memory_policy.md`
- `{AI_MEMORY_ROOT}/AI_CONTEXT/trust_policy.md`

### 当 `SKILLS_RO` 为 on

- `{AI_MEMORY_ROOT}/AI_CONTEXT/skills/engineering_spec_workflow.md`
- `{AI_MEMORY_ROOT}/AI_CONTEXT/skills/trust_and_verification.md`

### 当 `PROJECT_MEMORY_RO` 为 on

加载 `{AI_MEMORY_ROOT}/AI_CONTEXT/projects/<project>/` 下的项目文件。

### 当 `PROJECT_MEMORY_RW` 为 on

- 新的项目决策写入 `decisions.md`（candidate → 用户确认后 confirmed）
- 检测到的 memory 冲突写入 `conflicts.md`
- 用户纠正写入 `corrections.md`（candidate，确认后应用）
- 仅当 `PROJECT_MEMORY_RO = on` 且 `MEMORY_POLICY_RO = on` 时允许落盘；否则只输出 proposed diff / suggested update

### 当 `ROUTE_LOG_RW` 为 on

- 模糊检索的匹配结果写入 `route_log.md`
- 仅当 `PROJECT_MEMORY_RO = on` 时允许落盘；否则只在回答中说明匹配结果

---

## 通用规则

- 不加载 `{AI_MEMORY_ROOT}/reference/`
- 不加载 `{AI_MEMORY_ROOT}/AI_CONTEXT/` 下 switches 未开启的内容
- 写操作仅在对应 RW 开关为 on 时执行，否则只输出建议不落盘

---

## 本项目本地上下文

### 项目目标

<!-- 一句话描述 -->

### 本地关键文件

<!-- - `./src/` -->
<!-- - `./docs/` -->

### 项目决策

<!-- 参考 AI_MEMORY 的 decisions.md 格式 -->
