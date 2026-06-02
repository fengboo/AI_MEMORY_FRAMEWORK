# Codex Handoff Prompt

你现在要在 `AI_MEMORY_FRAMEWORK` repo 中实现一个小型结构升级，目标是：

1. 保持现有 Markdown-based AI memory framework 不被破坏；
2. 新增跨项目可复用 memory layer；
3. 新增 HTML site viewer，把 Markdown memory 渲染成人类可查看的 dashboard；
4. 不引入数据库、不引入复杂 Web app、不绑定特定 AI 产品。

## 背景

当前 repo 已有：

```text
AI_CONTEXT/
docs/
scripts/
templates/
AGENTS.md
README.md
```

当前系统以 `AI_CONTEXT/**/*.md` 作为 source of truth。不要改成 HTML 存储。HTML 只是生成出来的 view layer。

## 需要实现

### 1. 新增 reusable memory layer

创建：

```text
AI_CONTEXT/reusable/
├── README.md
├── flows/
├── tools/
├── patterns/
└── conventions/
```

并添加初始文件：

```text
AI_CONTEXT/reusable/flows/python_sim_data_analysis.md
AI_CONTEXT/reusable/tools/virtuoso_bridge.md
AI_CONTEXT/reusable/patterns/spec_first_workflow.md
AI_CONTEXT/reusable/conventions/markdown_doc_convention.md
```

每个文件使用 YAML front matter，字段至少包括：

```yaml
---
id:
type:
scope: reusable
status: draft
domain: []
tools: []
used_by_projects: []
related_flows: []
related_tools: []
trust_level: medium
last_reviewed:
---
```

### 2. 新增 site viewer

创建：

```text
site/
├── README.md
├── assets/
│   ├── style.css
│   └── app.js
└── generated/
    └── .gitkeep
```

### 3. 新增 build script

新增：

```text
scripts/build_site.py
```

功能：

- 扫描 `AI_CONTEXT/**/*.md`；
- 解析 YAML front matter；
- 渲染 Markdown body；
- 生成：
  - `site/generated/index.html`
  - `site/generated/projects.html`
  - `site/generated/reusable.html`
  - `site/generated/review_queue.html`
  - `site/generated/search_index.json`

要求：

- 不强依赖第三方库；
- 若 `yaml` 或 `markdown` package 不存在，脚本也要 fallback；
- 输出 HTML 应简洁、端庄，不要花哨；
- 不要把 HTML 当作 source of truth；
- generated HTML 顶部写清楚“Generated from Markdown”。

### 4. 更新文档

新增：

```text
docs/site_viewer_design.md
docs/reusable_memory_design.md
docs/implementation_plan.md
```

并在 `README.md` 中增加一个简短章节：

```markdown
## HTML site viewer and reusable memory

Markdown remains the canonical source of truth. The optional `/site` viewer renders AI_CONTEXT Markdown files into static HTML dashboards for human-friendly browsing, review, and navigation.

Cross-project reusable memories are stored under `AI_CONTEXT/reusable/` and can be referenced by projects through metadata such as `uses_flows`, `uses_tools`, `inherits_patterns`, and `inherits_conventions`.
```

### 5. Backward compatibility

必须保证：

- 旧项目没有 `uses_flows` 等字段不会报错；
- 原有 lint/link-check 脚本不应被破坏；
- 不删除或移动原有文件；
- 只新增能力。

## 验证

运行：

```bash
python -m py_compile scripts/build_site.py
python scripts/build_site.py
```

检查生成：

```text
site/generated/index.html
site/generated/projects.html
site/generated/reusable.html
site/generated/review_queue.html
site/generated/search_index.json
```

然后运行：

```bash
python -m http.server 8000
```

打开：

```text
http://localhost:8000/site/generated/index.html
```

## 实现策略

优先做最小可用，不要过度设计：

- 不要引入 React；
- 不要引入数据库；
- 不要引入 vector DB；
- 不要做登录系统；
- 不要做复杂权限系统；
- 不要改变 memory source format。

## 重要原则

```text
Project-based accumulation
+
Reusable-memory extraction
+
Cross-project linking
+
HTML multi-view browsing
```

一句话：

> 项目负责沉淀具体上下文；reusable layer 负责沉淀跨项目能力；site viewer 负责把二者连接起来供人类查看。
