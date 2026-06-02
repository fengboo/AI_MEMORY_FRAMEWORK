# Reusable Memory Layer 设计说明

## 1. 问题背景

原始 AI_MEMORY_FRAMEWORK 以 project 为主要组织方式：

```text
AI_CONTEXT/projects/<project>/
├── index.md
├── decisions.md
├── conflicts.md
├── corrections.md
├── open_questions.md
├── route_log.md
└── validation_plan.md
```

这适合记录项目上下文，但实际使用时会出现一个问题：

> 记忆、喜好、决策确实是在项目中积累的，但很多经验不是只属于单个项目，而是跨项目复用的。

例如：

- 项目 A 用 Python 分析 Spectre 仿真数据；
- 项目 B 用 Python 分析 ADC 测试数据；
- 项目 C 用 Python 分析 SerDes transient waveform；
- 多个项目都用 `virtuoso-bridge` 调用 Virtuoso；
- 多个项目都需要 Codex Handoff Pack；
- 多个项目都遵循“自然语言 → 结构化 spec → 实现 → 验证”的工作流。

如果这些知识全部塞进各自 project 目录，会导致：

- 重复记录；
- 项目之间的经验难以复用；
- 新项目启动时不知道该继承哪些 flow/tool；
- 工具经验散落在多个 project；
- AI 检索时容易漏掉跨项目能力。

## 2. 设计结论

在 `AI_CONTEXT/` 下新增：

```text
AI_CONTEXT/reusable/
├── flows/
├── tools/
├── patterns/
└── conventions/
```

含义：

```text
projects/     记录项目特定上下文
reusable/     记录跨项目可复用经验
index/        记录项目与 reusable memory 的关系
site/         提供多维查看视图
```

## 3. Reusable memory 类型

### 3.1 Flow Memory

记录“如何完成一类事情”。

示例：

```text
reusable/flows/python_sim_data_analysis.md
reusable/flows/spectre_result_extraction.md
reusable/flows/cdl_hierarchy_extraction.md
reusable/flows/codex_handoff_pack.md
```

典型内容：

- 适用场景；
- 输入；
- 输出；
- 标准步骤；
- 常见坑；
- 验证方法；
- 推荐工具；
- 已使用项目。

### 3.2 Tool Memory

记录“某个工具怎么用、有什么限制和坑”。

示例：

```text
reusable/tools/virtuoso_bridge.md
reusable/tools/cadence_virtuoso.md
reusable/tools/spectre.md
reusable/tools/codex.md
reusable/tools/python_analysis_stack.md
```

典型内容：

- 用途；
- 可用接口；
- 限制；
- 常见错误；
- 推荐调用方式；
- 关联 flow；
- 使用过的项目。

### 3.3 Pattern Memory

记录抽象工程模式。

示例：

```text
reusable/patterns/spec_first_workflow.md
reusable/patterns/review_queue_pattern.md
reusable/patterns/conflict_resolution_loop.md
reusable/patterns/supervisor_executor_split.md
```

### 3.4 Convention Memory

记录长期习惯和约定。

示例：

```text
reusable/conventions/markdown_doc_convention.md
reusable/conventions/python_script_style.md
reusable/conventions/simulation_plotting_convention.md
reusable/conventions/chinese_english_technical_writing.md
```

## 4. Metadata 规范

每个 reusable memory 文件建议使用如下 YAML front matter：

```yaml
---
id: python_sim_data_analysis
type: flow
scope: reusable
status: active
domain:
  - analog_ic
  - simulation
  - data_analysis
tools:
  - python
  - pandas
  - matplotlib
used_by_projects: []
related_flows: []
related_tools: []
trust_level: medium
last_reviewed: 2026-05-26
---
```

关键字段：

| 字段 | 含义 |
|---|---|
| `id` | 稳定 identifier |
| `type` | `flow` / `tool` / `pattern` / `convention` |
| `scope` | `global` / `reusable` / `project` |
| `status` | `draft` / `active` / `deprecated` |
| `domain` | 所属领域 |
| `tools` | 关联工具 |
| `used_by_projects` | 哪些项目使用过 |
| `trust_level` | 可信度 |
| `last_reviewed` | 最近审查日期 |

## 5. Project 如何引用 reusable memory

项目的 `index.md` 或 `project.md` 中新增：

```yaml
---
id: project_adc_sim_analysis
type: project
status: active
uses_flows:
  - python_sim_data_analysis
  - spectre_result_extraction
uses_tools:
  - python_analysis_stack
  - spectre
inherits_patterns:
  - spec_first_workflow
inherits_conventions:
  - simulation_plotting_convention
related_projects:
  - project_serdes_waveform_analysis
---
```

也可以新增 `links.md`：

```markdown
# Linked reusable memory

## Flows

- ../../reusable/flows/python_sim_data_analysis.md
- ../../reusable/flows/spectre_result_extraction.md

## Tools

- ../../reusable/tools/spectre.md
- ../../reusable/tools/python_analysis_stack.md

## Patterns

- ../../reusable/patterns/spec_first_workflow.md
```

## 6. 提升规则：什么时候从 project 提升到 reusable

建议规则：

> 当某条 memory 被两个或以上项目复用，或预计未来会复用，就应从 project memory 提升为 reusable memory，并由 project 通过 metadata 或 links 引用它。

具体判断：

### 放在 project 中

只对当前项目成立：

- 本项目 pass device 是 NMOS；
- 本项目不接受多个 EA；
- 本项目只处理 CSV，不处理 PSF；
- 本项目主极点放在 NMOS gate；
- 本项目服务于某个 ADC array。

### 放在 reusable 中

未来大概率会跨项目复用：

- Python 分析仿真数据 flow；
- Spectre 结果解析 flow；
- Virtuoso bridge 调用方式；
- Codex handoff pack 格式；
- Markdown 文档规范；
- schematic 可读性整理规则。

### 放在 global preference 中

长期用户偏好：

- 中文描述 + 英文 technical term；
- AI 先列 assumptions；
- spec-first workflow；
- 冲突不静默裁决；
- 关键 memory 需要 review。

## 7. 与 site viewer 的关系

HTML viewer 应支持多种视图：

```text
site/generated/index.html
site/generated/projects.html
site/generated/reusable.html
site/generated/review_queue.html
```

未来可以扩展：

```text
site/generated/tools.html
site/generated/flows.html
site/generated/patterns.html
site/generated/conventions.html
site/generated/graph.html
```

这样不再只能按 project 看，而可以从 tool / flow / pattern / convention 反向查看哪些项目使用了它。
