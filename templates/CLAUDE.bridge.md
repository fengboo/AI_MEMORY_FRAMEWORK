---
type: template
name: claude_bridge
scope: global
version: 0.3
description: 放在任何工程目录根下，作为 Claude Code 通向 AI_MEMORY 的桥梁
---

<!-- AI_MEMORY_ROOT = /path/to/AI_MEMORY -->
<!-- 使用时仅需修改上面这一个路径变量 -->

<!-- 只修改本文件顶部的 AI_MEMORY_ROOT 和 Bridge Switches。
     下方正文只是说明，不作为第二份配置。 -->

<!-- ============================================================
     Bridge Switches — 按项目需求调整 (on / off)
     ============================================================

     预设组合：
       小项目 / 临时任务：仅 GLOBAL_WORKFLOW_RO = on，其余全部 off
       中型项目：         GLOBAL_WORKFLOW_RO + SKILLS_RO = on，PROJECT_MEMORY_RO = on，只读不写
       大项目 / 长期：    全部 on（读写全开，经验积累）

     ============================================================ -->

<!-- 读开关 -->
<!-- GLOBAL_WORKFLOW_RO  = on -->   <!-- user_profile, workflow, constraints -->
<!-- MEMORY_POLICY_RO    = off -->  <!-- memory_policy, trust_policy -->
<!-- PROJECT_MEMORY_RO   = off -->  <!-- 项目级 decisions, conflicts, corrections, open_questions -->
<!-- SKILLS_RO           = on -->   <!-- engineering_spec_workflow, trust_and_verification -->

<!-- 写开关（仅在依赖读开关为 on 时生效） -->
<!-- PROJECT_MEMORY_RW   = off -->  <!-- 写入 decisions / conflicts / corrections -->
<!-- ROUTE_LOG_RW        = off -->  <!-- 写入 route_log -->

# 项目协作规则（Claude Code）

## Bridge Switches 说明

本文件顶部的 `Bridge Switches` 是唯一 authoritative config。需要改读写权限时，只改顶部注释块中的 `on / off`，不要改正文说明。

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

两个模板的开关结构完全一致，仅 agent 入口不同。

**典型场景（示例组合，不是当前配置）：**
```
小项目 / 临时：GLOBAL_WORKFLOW_RO = on，其余 off
中型项目：     GLOBAL_WORKFLOW_RO + SKILLS_RO + PROJECT_MEMORY_RO = on，只读不写
大项目 / 长期：全部 on
```

---

## 全局上下文

以下加载行为由顶部 switches 控制。

### 当 `GLOBAL_WORKFLOW_RO` 为 on

- `{AI_MEMORY_ROOT}/AI_CONTEXT/user_profile.md`
- `{AI_MEMORY_ROOT}/AI_CONTEXT/workflow.md`
- `{AI_MEMORY_ROOT}/AI_CONTEXT/constraints.md`

### 当 `MEMORY_POLICY_RO` 为 on

- `{AI_MEMORY_ROOT}/AI_CONTEXT/memory_policy.md`
- `{AI_MEMORY_ROOT}/AI_CONTEXT/trust_policy.md`

### 当 `SKILLS_RO` 为 on

- `{AI_MEMORY_ROOT}/AI_CONTEXT/skills/engineering_spec_workflow.md`
- `{AI_MEMORY_ROOT}/AI_CONTEXT/skills/trust_and_verification.md`

### 当 `PROJECT_MEMORY_RO` 为 on

加载 `{AI_MEMORY_ROOT}/AI_CONTEXT/projects/<project>/` 下的项目文件。

### 当 `PROJECT_MEMORY_RW` 为 on

- decisions → `decisions.md`（candidate → confirmed）
- 冲突 → `conflicts.md`
- 纠正 → `corrections.md`（candidate，确认后应用）
- 仅当 `PROJECT_MEMORY_RO = on` 且 `MEMORY_POLICY_RO = on` 时允许落盘；否则只输出 proposed diff / suggested update

### 当 `ROUTE_LOG_RW` 为 on

- 检索匹配结果 → `route_log.md`
- 仅当 `PROJECT_MEMORY_RO = on` 时允许落盘；否则只在回答中说明匹配结果

---

## 通用规则

- 不加载 `{AI_MEMORY_ROOT}/reference/`
- 不加载 switches 未开启的内容
- 写操作仅在对应 RW 开关为 on 时执行

---

## 本项目上下文

<!-- 以下按需填写 -->
