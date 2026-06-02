# AI Memory System

可移植的 AI 协作上下文层 —— 基于 Markdown 文件树的 AI agent memory、workflow 和 governance 系统。

## 这是什么

一套**跨模型、跨平台、人类可读**的 AI 协作基础设施。它不绑定任何特定 AI 产品或 API，而是用纯 Markdown + YAML front matter 文件树来存储：

- **用户偏好与工作流规则**（user profile、workflow、constraints）
- **长期记忆与项目决策**（decisions、assumptions、conflicts、corrections）
- **可信度与验证机制**（trust labels、validation plan）
- **多角色协作通道**（用户 / 监工 AI / 执行 AI 的 supervision channel）

核心思想：**不要把 AI 当成一次性问答工具，而要把它组织成一个可审查、可迁移、可验证、可迭代的工程协作系统。**

## 适用场景

- 需要跨 Codex / Claude / Cursor 等多个 AI 工具保持一致的工程上下文
- 长期项目需要持久化的 memory governance（决策追溯、冲突裁决、纠正闭环）
- 需要用户 + 监工 AI + 执行 AI 三方协作的复杂工程任务
- 想要控制 AI 的工作方式（progressive spec workflow、可信度标注、验证闭环）

## 文件结构

```
AI_MEMORY/
├── README.md                              ← 你正在读的文件（给人看）
├── AGENTS.md                              ← AI agent 入口点（给 AI 看）
├── AI_CONTEXT/                            ← AI 操作文件（agent 日常加载）
│   ├── README.md                          ←   加载路由指南
│   ├── user_profile.md                    ←   用户偏好模板（使用前填写）
│   ├── workflow.md                        ←   渐进式规格工作流定义
│   ├── constraints.md                     ←   项目约束（做什么、不做什么）
│   ├── memory_policy.md                   ←   memory 治理策略 + 健康检查清单
│   ├── trust_policy.md                    ←   可信度标注规范
│   ├── TODO.md                            ←   总体 TODO（Phase 0-5）
│   ├── skills/
│   │   ├── engineering_spec_workflow.md   ←   Skill：工程规格工作流
│   │   └── trust_and_verification.md      ←   Skill：可信度与验证
│   ├── reusable/                          ←   跨项目可复用 memory（flows / tools / patterns / conventions）
│   └── projects/
│       ├── index.md                       ←   项目索引 + 检索规则
│       └── example_project/               ←   示例项目（展示机制用法）
│           ├── index.md
│           ├── decisions.md
│           ├── conflicts.md
│           ├── corrections.md
│           ├── open_questions.md
│           ├── route_log.md
│           ├── validation_plan.md
│           └── supervision/               ←   多角色协作通道（可选）
├── scripts/                               ← 验证工具脚本
│   ├── ai_context_lint.py                 ←   front matter 完整性检查
│   ├── ai_context_link_check.py           ←   内部链接有效性检查
│   ├── bridge_config_check.py             ←   bridge 开关配置校验
│   └── build_site.py                      ←   生成 HTML site viewer
├── site/                                  ← HTML 查看层（generated，不是 source of truth）
├── templates/                             ← 桥接模板（复制到工程目录用）
│   ├── AGENTS.bridge.md                   ←   Codex / AGENTS.md 生态用
│   ├── CLAUDE.bridge.md                   ←   Claude Code 用
│   └── lifecycle_metadata_template.md     ←   future lifecycle metadata 参考模板
└── docs/                                  ← 补充文档
    ├── method_overview.md                 ←   方法论概述
    └── phase5_advanced_options.md         ←   Phase 5 高级特性说明
```

## 快速开始

### 给人用

1. 填写 `AI_CONTEXT/user_profile.md` — 你的语言、工作流、信任偏好
2. 阅读 `AI_CONTEXT/workflow.md` — 了解 AI 将如何工作
3. 阅读 `docs/method_overview.md` — 了解方法论背景（可选）

### 给 AI agent 用

本仓库是**集中式上下文存储**。你的工程项目通过桥接文件指向这里。

**第一步**：将 AI_MEMORY clone 到本地固定路径：
```bash
git clone <your-repo-url> /path/to/AI_MEMORY
```

**第二步**：在你的工程项目根目录放置桥接文件：
- 用 Codex/AGENTS.md 生态 → 复制 `templates/AGENTS.bridge.md` 到项目根目录，重命名为 `AGENTS.md`
- 用 Claude Code → 复制 `templates/CLAUDE.bridge.md` 到项目根目录，重命名为 `CLAUDE.md`
- 修改桥接文件顶部的 `AI_MEMORY_ROOT` 为实际路径

**第三步**：根据项目类型调整 bridge 顶部的读/写开关：

| 场景 | 配置 |
|---|---|
| 小项目 / 临时 | `GLOBAL_WORKFLOW_RO = on`，其余 off — 只读工作流，不碰记忆 |
| 中型项目 | 加上 `SKILLS_RO + PROJECT_MEMORY_RO = on` — 读项目记忆，只读不写 |
| 大项目 / 长期 | 全部 on — 读写全开，但关键 memory 仍需用户 review |

**开关说明：**

| 开关 | 控制 | 默认 | 依赖 |
|---|---|---|---|
| `GLOBAL_WORKFLOW_RO` | user_profile, workflow, constraints | on | — |
| `MEMORY_POLICY_RO` | memory_policy, trust_policy | off | — |
| `PROJECT_MEMORY_RO` | 项目级 decisions, conflicts, corrections, open_questions | off | — |
| `SKILLS_RO` | engineering_spec_workflow, trust_and_verification | on | — |
| `PROJECT_MEMORY_RW` | 写入 decisions / conflicts / corrections | off | `PROJECT_MEMORY_RO=on` 且 `MEMORY_POLICY_RO=on` |
| `ROUTE_LOG_RW` | 写入 route_log | off | `PROJECT_MEMORY_RO=on` |

当 RW 开关为 off 时，agent 只能输出 proposed diff / suggested update，不写入 AI_MEMORY。

### 多角色协作模式（可选）

| 角色 | 职责 |
|---|---|
| 用户 | 最终裁决关键方向、冲突、memory 更新 |
| 监工 AI | 把握项目方向，在大节点 review |
| 执行 AI | 按 brief 推进实现、测试、记录 |

交互流程：`用户/监工 → EXECUTOR_BRIEF → 执行 AI → HANDOFF_LOG → 监工 review → 用户确认`

## 核心原则

1. **不要隐藏假设** — AI 的推断假设必须显式标注 `[ASSUME]`，让用户 review
2. **冲突落盘，不静默裁决** — 矛盾 memory 写入 `conflicts.md`，用户保留最终裁决权
3. **纠正闭环** — 用户纠正 AI 后，写入 `corrections.md` candidate，确认后更新
4. **有工具验证 > AI 自述验证 > 无验证** — 能用真实 toolchain 验证的不依赖 AI 自我报告
5. **读/写开关控制权限** — 小项目只读不写，大项目才开启 memory 积累

## 验证命令

```bash
# Front matter 完整性（推荐 --strict + --json 做 CI 集成）
python scripts/ai_context_lint.py --strict
python scripts/ai_context_lint.py --strict --json

# 内部链接有效性（--all 扫描全树，--anchors 检查锚点片段）
python scripts/ai_context_link_check.py
python scripts/ai_context_link_check.py --all --anchors --json

# Bridge 模板开关配置校验（--all 检查所有 bridge 文件）
python scripts/bridge_config_check.py templates/AGENTS.bridge.md
python scripts/bridge_config_check.py --all

# Python 语法检查
python -m py_compile scripts/ai_context_lint.py
python -m py_compile scripts/ai_context_link_check.py
python -m py_compile scripts/bridge_config_check.py
```

## 刻意不包括的内容

- 不绑定特定 AI 产品
- 不包含真实用户偏好或项目数据（`example_project/` 是纯示例）
- 不包含 RAG / vector retrieval / schema orchestration（见 `docs/phase5_advanced_options.md`）
- 不包含自动化 memory 改写

## 当前状态

本仓库是脱敏后的通用框架。Phase 0-4 的机制已实施并可复用。Phase 5 advanced features 记录在 `docs/phase5_advanced_options.md` 中但未实现。

## HTML site viewer and reusable memory

Markdown remains the canonical source of truth. The optional `site/` viewer renders `AI_CONTEXT/**/*.md` into static HTML dashboards for human-friendly browsing, review, and navigation.

Cross-project reusable memories are stored under `AI_CONTEXT/reusable/` and organized as `flows/`, `tools/`, `patterns/`, and `conventions`. Projects can reference reusable memory through metadata such as `uses_flows`, `uses_tools`, `inherits_patterns`, and `inherits_conventions`.

Build the viewer with:

```bash
python scripts/build_site.py
```

Generated HTML and JSON under `site/generated/` are view/cache artifacts. Do not treat them as the authoritative memory source.

## Future memory lifecycle

当前框架暂不实现完整的 memory lifecycle / compression / archive 机制。未来当项目数量、route log、reusable memory 和历史决策增长到产生真实噪声时，可在现有 Markdown 文件树上追加 `active / warm / cold / archived / deprecated / superseded` lifecycle state、raw log → summary → reusable pattern 的压缩路径、memory health dashboard 和 retrieval policy。

当前合入的 lifecycle 内容只是 future upgrade design，不改变主流程、不迁移历史文件、不修改 bridge 加载逻辑。

See:

- `docs/future_memory_lifecycle_design.md`
- `docs/memory_lifecycle_policy_draft.md`
- `docs/future_upgrade_trigger_conditions.md`

## 许可

MIT License — 见 [LICENSE](LICENSE)。

## 参考

- 方法论概述：`docs/method_overview.md`
- Phase 5 高级选项：`docs/phase5_advanced_options.md`
- OpenAI Codex `AGENTS.md` guide
- AGENTS.md open format
