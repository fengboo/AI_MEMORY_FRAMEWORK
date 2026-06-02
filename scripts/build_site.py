#!/usr/bin/env python3
"""
Build static HTML viewer for AI_MEMORY_FRAMEWORK.

Usage:
    python scripts/build_site.py

Principles:
    Markdown is the source of truth.
    site/generated/*.html is generated view/cache.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
AI_CONTEXT = ROOT / "AI_CONTEXT"
SITE = ROOT / "site"
ASSETS = SITE / "assets"
GENERATED = SITE / "generated"


@dataclass
class MemoryDoc:
    path: str
    rel_path: str
    title: str
    body: str
    html_body: str
    metadata: Dict[str, Any]
    doc_type: str
    scope: str
    status: str
    trust_level: str


def parse_front_matter(text: str) -> Tuple[Dict[str, Any], str]:
    """Parse minimal YAML front matter.

    Uses PyYAML if available. Falls back to a small parser supporting:
    - key: value
    - key: []
    - key:
        - item
    """
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    raw = text[4:end].strip()
    body = text[end + len("\n---"):].lstrip("\n")

    try:
        import yaml  # type: ignore
        data = yaml.safe_load(raw) or {}
        if isinstance(data, dict):
            return data, body
    except Exception:
        pass

    data: Dict[str, Any] = {}
    current_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        current_key = key
        if val == "[]":
            data[key] = []
        elif val == "":
            data[key] = []
        elif val in ("true", "false"):
            data[key] = val == "true"
        else:
            data[key] = val.strip('"').strip("'")
    return data, body


def simple_markdown_to_html(md: str) -> str:
    """Small Markdown renderer fallback.

    This is intentionally conservative. If python-markdown is installed,
    markdown_to_html() will use it instead.
    """
    lines = md.splitlines()
    out: List[str] = []
    in_code = False
    code_buf: List[str] = []
    in_ul = False
    in_ol = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    for line in lines:
        if line.startswith("```"):
            if not in_code:
                close_lists()
                in_code = True
                code_buf = []
            else:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                in_code = False
            continue

        if in_code:
            code_buf.append(line)
            continue

        if not line.strip():
            close_lists()
            continue

        if line.startswith("#"):
            close_lists()
            level = min(len(line) - len(line.lstrip("#")), 6)
            text = line[level:].strip()
            out.append(f"<h{level}>{inline(text)}</h{level}>")
            continue

        if line.startswith("- "):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(line[2:].strip())}</li>")
            continue

        if re.match(r"^\d+\.\s+", line):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s+", "", line)
            out.append(f"<li>{inline(item.strip())}</li>")
            continue

        close_lists()
        out.append(f"<p>{inline(line.strip())}</p>")

    close_lists()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def markdown_to_html(md: str) -> str:
    try:
        import markdown  # type: ignore
        return markdown.markdown(md, extensions=["fenced_code", "tables", "toc"])
    except Exception:
        return simple_markdown_to_html(md)


def title_from_body_or_path(body: str, path: Path, metadata: Dict[str, Any]) -> str:
    if metadata.get("title"):
        return str(metadata["title"])
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def classify_doc(path: Path, metadata: Dict[str, Any]) -> Tuple[str, str]:
    doc_type = str(metadata.get("type") or "")
    scope = str(metadata.get("scope") or "")

    rel = path.relative_to(AI_CONTEXT).as_posix()
    if not scope:
        if rel.startswith("projects/"):
            scope = "project"
        elif rel.startswith("reusable/"):
            scope = "reusable"
        else:
            scope = "global"

    if not doc_type:
        parts = rel.split("/")
        if "reusable" in parts:
            doc_type = parts[1][:-1] if len(parts) > 2 and parts[1].endswith("s") else "reusable"
        elif "projects" in parts:
            doc_type = "project"
        else:
            doc_type = "document"

    return doc_type, scope


def load_docs() -> List[MemoryDoc]:
    docs: List[MemoryDoc] = []
    if not AI_CONTEXT.exists():
        raise SystemExit(f"Missing AI_CONTEXT directory: {AI_CONTEXT}")

    for path in sorted(AI_CONTEXT.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        metadata, body = parse_front_matter(text)
        doc_type, scope = classify_doc(path, metadata)
        title = title_from_body_or_path(body, path, metadata)
        rel_path = path.relative_to(ROOT).as_posix()
        docs.append(
            MemoryDoc(
                path=str(path),
                rel_path=rel_path,
                title=title,
                body=body,
                html_body=markdown_to_html(body),
                metadata=metadata,
                doc_type=doc_type,
                scope=scope,
                status=str(metadata.get("status", "")),
                trust_level=str(metadata.get("trust_level", "")),
            )
        )
    return docs


def page_shell(title: str, body: str) -> str:
    css_path = "../assets/style.css"
    js_path = "../assets/app.js"
    nav = """
      <h1>AI Memory</h1>
      <a href="index.html">Overview</a>
      <a href="projects.html">Projects</a>
      <a href="reusable.html">Reusable</a>
      <a href="review_queue.html">Review Queue</a>
      <a href="search_index.json">JSON Index</a>
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      {nav}
    </aside>
    <main>
      <div class="generated-note">Generated from Markdown. Do not edit generated HTML directly.</div>
      {body}
    </main>
  </div>
  <script src="{js_path}"></script>
</body>
</html>
"""


def badge(text: Any) -> str:
    if text in (None, "", []):
        return ""
    return f'<span class="badge">{html.escape(str(text))}</span>'


def doc_card(doc: MemoryDoc) -> str:
    meta = []
    if doc.scope:
        meta.append(badge(f"scope: {doc.scope}"))
    if doc.doc_type:
        meta.append(badge(f"type: {doc.doc_type}"))
    if doc.status:
        meta.append(badge(f"status: {doc.status}"))
    if doc.trust_level:
        meta.append(badge(f"trust: {doc.trust_level}"))

    mid = doc.metadata.get("id", "")
    id_part = f"<p class='meta'>id: <code>{html.escape(str(mid))}</code></p>" if mid else ""
    return f"""
    <article class="card searchable-item">
      <h3>{html.escape(doc.title)}</h3>
      <p class="meta"><code>{html.escape(doc.rel_path)}</code></p>
      {id_part}
      <div>{''.join(meta)}</div>
    </article>
    """


def overview_page(docs: List[MemoryDoc]) -> str:
    counts: Dict[str, int] = {}
    for d in docs:
        counts[d.scope] = counts.get(d.scope, 0) + 1

    cards = "".join(
        f"""
        <div class="card">
          <h2>{html.escape(scope.title())}</h2>
          <p style="font-size:32px; margin: 0;">{count}</p>
          <p class="meta">Markdown documents</p>
        </div>
        """
        for scope, count in sorted(counts.items())
    )

    recent = "".join(doc_card(d) for d in docs[:12])
    body = f"""
    <h1>AI Memory Dashboard</h1>
    <p>这是从 <code>AI_CONTEXT/**/*.md</code> 生成的静态 HTML 查看层。Markdown 仍然是唯一可信源。</p>
    <div class="grid">{cards}</div>
    <h2>Search</h2>
    <input id="search" class="search" placeholder="Filter visible cards...">
    <h2>Documents</h2>
    <div>{recent}</div>
    <script>window.addEventListener("load", function () {{ aiMemorySearch("search", ".searchable-item"); }});</script>
    """
    return page_shell("AI Memory Dashboard", body)


def listing_page(title: str, docs: List[MemoryDoc]) -> str:
    cards = "".join(doc_card(d) for d in docs)
    body = f"""
    <h1>{html.escape(title)}</h1>
    <input id="search" class="search" placeholder="Filter...">
    <div>{cards or '<p>No documents found.</p>'}</div>
    <script>window.addEventListener("load", function () {{ aiMemorySearch("search", ".searchable-item"); }});</script>
    """
    return page_shell(title, body)


def review_queue_page(docs: List[MemoryDoc]) -> str:
    keywords = ("conflict", "correction", "open_question", "question")
    queue = []
    for d in docs:
        rel = d.rel_path.lower()
        status = d.status.lower()
        trust = d.trust_level.lower()
        if (
            any(k in rel for k in keywords)
            or status in {"pending", "candidate", "draft", "needs_review"}
            or trust == "low"
        ):
            queue.append(d)

    cards = "".join(doc_card(d) for d in queue)
    body = f"""
    <h1>Review Queue</h1>
    <p>该页面聚合可能需要人类 review 的 memory：conflicts、corrections、open_questions、draft/pending/candidate/low-trust 等。</p>
    <input id="search" class="search" placeholder="Filter review items...">
    <div>{cards or '<p>No review items found.</p>'}</div>
    <script>window.addEventListener("load", function () {{ aiMemorySearch("search", ".searchable-item"); }});</script>
    """
    return page_shell("Review Queue", body)


def build_index(docs: List[MemoryDoc]) -> List[Dict[str, Any]]:
    index = []
    for d in docs:
        item = {
            "title": d.title,
            "rel_path": d.rel_path,
            "type": d.doc_type,
            "scope": d.scope,
            "status": d.status,
            "trust_level": d.trust_level,
            "metadata": d.metadata,
        }
        index.append(item)
    return index


def write_outputs(docs: List[MemoryDoc]) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    (GENERATED / "index.html").write_text(overview_page(docs), encoding="utf-8")
    (GENERATED / "projects.html").write_text(
        listing_page("Projects", [d for d in docs if d.scope == "project" or "/projects/" in d.rel_path]),
        encoding="utf-8",
    )
    (GENERATED / "reusable.html").write_text(
        listing_page("Reusable Memory", [d for d in docs if d.scope == "reusable" or "/reusable/" in d.rel_path]),
        encoding="utf-8",
    )
    (GENERATED / "review_queue.html").write_text(review_queue_page(docs), encoding="utf-8")
    (GENERATED / "search_index.json").write_text(
        json.dumps(build_index(docs), ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def main() -> None:
    global ROOT, AI_CONTEXT, SITE, ASSETS, GENERATED

    parser = argparse.ArgumentParser(description="Build AI Memory static HTML site.")
    parser.add_argument("--root", default=str(ROOT), help="Repo root. Default: inferred from script path.")
    args = parser.parse_args()

    ROOT = Path(args.root).resolve()
    AI_CONTEXT = ROOT / "AI_CONTEXT"
    SITE = ROOT / "site"
    ASSETS = SITE / "assets"
    GENERATED = SITE / "generated"

    docs = load_docs()
    write_outputs(docs)
    print(f"Built {len(docs)} docs into {GENERATED}")


if __name__ == "__main__":
    main()
