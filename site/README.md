# AI Memory Site Viewer

`site/` 是 AI_MEMORY_FRAMEWORK 的 HTML 查看层。

## 原则

```text
Markdown = source of truth
HTML = generated view
JSON = generated index
```

不要直接修改 `site/generated/*.html` 中的内容。若需要更新内容，请修改 `AI_CONTEXT/**/*.md` 后重新运行：

```bash
python scripts/build_site.py
```

## 本地查看

```bash
python scripts/build_site.py
python -m http.server 8000
```

然后打开：

```text
http://localhost:8000/site/generated/index.html
```

## 目录

```text
site/
├── README.md
├── assets/
│   ├── style.css
│   └── app.js
└── generated/
    ├── index.html
    ├── projects.html
    ├── reusable.html
    ├── review_queue.html
    └── search_index.json
```
