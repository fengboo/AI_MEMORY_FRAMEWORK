# Site Viewer 设计说明

## 1. 问题背景

AI_MEMORY_FRAMEWORK 当前使用 Markdown + YAML front matter 文件树来保存 AI 协作上下文、项目决策、冲突、纠正和工作流规则。这种方式非常适合作为长期存储格式：

- AI agent 容易读写；
- Git diff 清晰；
- 跨模型、跨平台；
- 人类可直接审查；
- 不绑定数据库、Web app 或某个 AI 产品。

但实际使用时，纯 Markdown 文件树会遇到浏览体验问题：

- 项目多了以后难以全局浏览；
- `decisions.md`、`conflicts.md`、`corrections.md` 分散在不同目录；
- YAML metadata 对 AI 友好，但对人类阅读不够直观；
- 需要 dashboard、timeline、review queue、cross-project graph 等视图；
- 用户需要快速知道哪些 memory 需要 review、哪些项目复用了某个 flow/tool。

因此应新增 `site/` 目录作为 HTML 查看层。

## 2. 设计结论

采用：

```text
AI_CONTEXT/**/*.md
        ↓
scripts/build_site.py
        ↓
site/generated/*.html
site/generated/search_index.json
```

其中：

```text
Markdown = 唯一可信源 source of truth
HTML = 生成的查看层 view layer
JSON = 生成的索引 cache
```

## 3. 目录建议

```text
AI_MEMORY_FRAMEWORK/
├── AI_CONTEXT/
│   ├── user_profile.md
│   ├── workflow.md
│   ├── constraints.md
│   ├── projects/
│   └── reusable/
│       ├── flows/
│       ├── tools/
│       ├── patterns/
│       └── conventions/
│
├── scripts/
│   ├── ai_context_lint.py
│   ├── ai_context_link_check.py
│   ├── bridge_config_check.py
│   └── build_site.py
│
├── site/
│   ├── README.md
│   ├── assets/
│   │   ├── style.css
│   │   └── app.js
│   └── generated/
│       ├── index.html
│       ├── projects.html
│       ├── reusable.html
│       ├── review_queue.html
│       └── search_index.json
│
└── docs/
    ├── method_overview.md
    ├── reusable_memory_design.md
    └── site_viewer_design.md
```

## 4. 两种查看模式

### 4.1 Static build 模式

先运行：

```bash
python scripts/build_site.py
```

再打开：

```text
site/generated/index.html
```

优点：

- 简单稳定；
- 可部署到 GitHub Pages；
- 可生成跨项目索引；
- 适合 dashboard / review queue / timeline。

缺点：

- Markdown 更新后需要重新 build。

### 4.2 Runtime viewer 模式

浏览器打开 `site/index.html`，由 JavaScript 直接 fetch Markdown 并渲染。

优点：

- 不必为每个 Markdown 预生成 HTML；
- 页面可以动态加载。

限制：

- 直接双击本地 HTML 通常不能读取本地 Markdown；
- 需要本地 HTTP server 或 GitHub Pages；
- 复杂统计、全局索引、cross-project graph 仍然更适合 build script。

## 5. 推荐实现顺序

```text
P0: build_site.py 生成静态 HTML dashboard
P1: 生成 search_index.json
P2: site/assets/app.js 支持前端搜索/filter
P3: 支持 runtime Markdown fetch
P4: 支持 graph view / relation map
```

当前交付包实现的是 P0 + P1 的最小可用版本。
