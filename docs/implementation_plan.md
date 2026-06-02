# 实施计划

## Phase 0 — 保持原结构不破坏

目标：

- 不删除原有 `AI_CONTEXT/projects/`；
- 不修改现有 lint/link-check 脚本的行为；
- 不改变 AGENTS bridge 的基本加载方式。

行动：

```text
只新增目录和脚本，不重构既有文件。
```

## Phase 1 — 新增 reusable layer

新增：

```text
AI_CONTEXT/reusable/
├── README.md
├── flows/
├── tools/
├── patterns/
└── conventions/
```

并放入初始模板：

```text
flows/python_sim_data_analysis.md
tools/virtuoso_bridge.md
patterns/spec_first_workflow.md
conventions/markdown_doc_convention.md
```

## Phase 2 — 新增 site viewer

新增：

```text
site/
├── README.md
├── assets/
│   ├── style.css
│   └── app.js
└── generated/
    └── .gitkeep
```

新增脚本：

```text
scripts/build_site.py
```

脚本功能：

1. 扫描 `AI_CONTEXT/**/*.md`；
2. 解析 YAML front matter；
3. 渲染 Markdown body；
4. 生成：
   - `site/generated/index.html`
   - `site/generated/projects.html`
   - `site/generated/reusable.html`
   - `site/generated/review_queue.html`
   - `site/generated/search_index.json`

## Phase 3 — Project metadata 扩展

在 project `index.md` 中可选新增：

```yaml
uses_flows: []
uses_tools: []
inherits_patterns: []
inherits_conventions: []
related_projects: []
```

保持 backward compatible：旧项目没有这些字段也不报错。

## Phase 4 — Review queue

根据 front matter 和文件路径聚合：

- `conflicts.md`
- `corrections.md`
- `open_questions.md`
- `status: pending`
- `status: candidate`
- `trust_level: low`

生成 `review_queue.html`。

## Phase 5 — 前端增强

在 `site/assets/app.js` 中支持：

- 搜索；
- filter；
- 按 `type/scope/status/domain/tool/project` 分类；
- 后续可加 graph view。

## 验证命令

```bash
python -m py_compile scripts/build_site.py
python scripts/build_site.py
python -m http.server 8000
```

打开：

```text
http://localhost:8000/site/generated/index.html
```

## 预期输出

```text
site/generated/index.html
site/generated/projects.html
site/generated/reusable.html
site/generated/review_queue.html
site/generated/search_index.json
```

## Git 策略

两种选择：

### 方案 A：提交 generated HTML

适合 GitHub Pages：

```text
site/generated/*.html 提交到 Git
```

优点：线上可直接看。  
缺点：每次改 Markdown 后需要重新生成并提交。

### 方案 B：不提交 generated HTML

适合本地 viewer：

```gitignore
site/generated/*
!site/generated/.gitkeep
```

优点：repo 干净。  
缺点：不能直接用 GitHub Pages 看生成结果。

推荐当前阶段：

```text
site/assets/ 提交
site/generated/ 暂时也可以提交，方便 GitHub Pages 和人工查看
```
