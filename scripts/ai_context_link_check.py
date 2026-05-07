"""Link checker for AI_CONTEXT/ internal references.

Checks that:
  1. [text](path) markdown links point to existing files
  2. Project index "Key Files" entries exist relative to the project directory

Modes:
  default  — scans index files only (fast, backward-compatible)
  --all    — scans all .md files under AI_CONTEXT/ and AI_MEMORY/ root

Options:
  --json   — output results as JSON (default: human-readable)
  --anchors — check that local Markdown anchors (#fragment) exist in target files

Usage: python scripts/ai_context_link_check.py [--all] [--json] [--anchors] [--root <path>]
"""

import re
import sys
import json
from pathlib import Path


def _find_root() -> Path:
    """Find AI_MEMORY root. Checks --root arg first, then script location."""
    for i, arg in enumerate(sys.argv):
        if arg == "--root" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1]).resolve()
    return Path(__file__).resolve().parent.parent


AI_MEMORY_ROOT = _find_root()
AI_CONTEXT = AI_MEMORY_ROOT / "AI_CONTEXT"
SKIP_DIRS = {"reference", "templates", "scripts", ".git"}


def extract_md_links(text: str) -> list[tuple[str, str]]:
    """Extract (path, context_hint) from [text](path) markdown links."""
    results = []
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        path = m.group(2).strip()
        if not path or path.startswith(("http://", "https://", "#")):
            continue
        # Split anchor
        path = path.split("#")[0]
        results.append((path, "link"))
    return results


def extract_md_links_with_anchors(text: str) -> list[tuple[str, str | None]]:
    """Extract (path, anchor_or_None) from [text](path#anchor) links."""
    results = []
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        target = m.group(2).strip()
        if not target or target.startswith(("http://", "https://")):
            continue
        if target.startswith("#"):
            continue  # same-page anchor, skip
        if "#" in target:
            path, anchor = target.split("#", 1)
            results.append((path, anchor))
        else:
            results.append((target, None))
    return results


def extract_key_files(text: str) -> list[str]:
    """Extract filenames from Key Files / 关键文件 section in project index.

    Matches lines like:
      - `decisions.md` — description
      - `supervision/` — description
    """
    results = []
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()

        if re.search(r"(Key Files|关键文件)", stripped):
            in_section = True
            continue

        if not in_section:
            continue

        if stripped.startswith("##"):
            in_section = False
            continue

        m = re.match(r"-\s+`([^`]+)`", stripped)
        if m:
            ref = m.group(1)
            if ref.endswith((".md", "/")):
                results.append(ref)
            continue

        m = re.match(r"-\s+([\w\-/]+\.md)", stripped)
        if m:
            results.append(m.group(1))
            continue

        if stripped and not stripped.startswith("- "):
            in_section = False

    return results


def is_project_index(path: Path) -> bool:
    """Check if `path` is a project-level index.md (under projects/<name>/).

    Uses path depth relative to AI_CONTEXT/projects/ to avoid fragile
    parent-name checks.
    """
    try:
        rel = path.relative_to(AI_CONTEXT / "projects")
    except ValueError:
        return False
    # Project index: projects/<project>/index.md → depth 2
    # Sub-category: projects/<cat>/<project>/index.md → depth 3
    return path.name == "index.md" and len(rel.parts) >= 2


def resolve(path: Path, ref: str) -> Path | None:
    """Resolve a reference. Returns existing Path or None."""
    candidate = (path.parent / ref).resolve()
    if candidate.exists():
        return candidate
    candidate = (AI_CONTEXT / ref).resolve()
    if candidate.exists():
        return candidate
    candidate = (AI_MEMORY_ROOT / ref).resolve()
    if candidate.exists():
        return candidate
    return None


def check_anchor(target_file: Path, anchor: str) -> bool:
    """Check if an anchor exists in a Markdown file.

    Supports: headings (#heading-text) and manual <a id="..."> anchors.
    """
    try:
        text = target_file.read_text(encoding="utf-8")
    except Exception:
        return False

    # Check headings: generate slug from heading text
    slug = anchor.lower().replace(" ", "-")
    slug = re.sub(r"[^\w\-]", "", slug)

    heading_patterns = [
        re.compile(rf"^#+\s+{re.escape(anchor)}$", re.MULTILINE | re.IGNORECASE),
        # Also try with ID attribute: <h2 id="anchor">
        re.compile(rf'id="{re.escape(anchor)}"'),
        re.compile(rf"id='{re.escape(anchor)}'"),
        # Try slug match from common heading→slug conventions
        re.compile(rf"^#+\s+.*$", re.MULTILINE),
    ]

    # Direct match on heading text
    if heading_patterns[0].search(text):
        return True

    # Direct ID match
    if heading_patterns[1].search(text) or heading_patterns[2].search(text):
        return True

    # Try slug-based heading match
    for h in heading_patterns[3].finditer(text):
        h_text = h.group(0).lstrip("#").strip().lower()
        h_text = re.sub(r"[^\w\-]", "", h_text.replace(" ", "-"))
        if h_text == slug:
            return True

    return False


def check_file(path: Path, check_key_files: bool = True, check_anchors: bool = False) -> list[str]:
    """Return broken references for this file."""
    broken = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return [f"cannot read file"]

    # Check [text](path) links (with optional anchor)
    if check_anchors:
        for ref, anchor in extract_md_links_with_anchors(text):
            if not ref:  # same-page anchor
                continue
            target = resolve(path, ref)
            if not target:
                label = f" → {ref}#{anchor}" if anchor else f" → {ref}"
                broken.append(f"[link]{label}")
            elif anchor and target.suffix == ".md":
                if not check_anchor(target, anchor):
                    broken.append(f"[anchor] → {ref}#{anchor}")
    else:
        for ref, _ctx in extract_md_links(text):
            if not resolve(path, ref):
                broken.append(f"[link] → {ref}")

    # For project index.md, check Key Files section
    if check_key_files and is_project_index(path):
        for ref in extract_key_files(text):
            candidate = path.parent / ref
            if not candidate.exists():
                broken.append(f"[key file] → {ref}")

    return broken


def scan_all_files(check_anchors: bool = False) -> dict[str, list[str]]:
    """Scan all .md files under AI_CONTEXT/ and root-level .md files."""
    all_broken: dict[str, list[str]] = {}
    scanned = 0

    # Root-level .md files (e.g. README.md, AGENTS.md)
    for md_file in sorted(AI_MEMORY_ROOT.glob("*.md")):
        broken = check_file(md_file, check_key_files=False, check_anchors=check_anchors)
        scanned += 1
        if broken:
            all_broken[str(md_file.relative_to(AI_MEMORY_ROOT))] = broken

    # AI_CONTEXT/ .md files
    for md_file in sorted(AI_CONTEXT.rglob("*.md")):
        parts = md_file.relative_to(AI_CONTEXT).parts
        if parts and parts[0] in SKIP_DIRS:
            continue
        if any(p.startswith(".") for p in parts):
            continue

        broken = check_file(md_file, check_key_files=True, check_anchors=check_anchors)
        scanned += 1
        if broken:
            all_broken[str(md_file.relative_to(AI_MEMORY_ROOT))] = broken

    return all_broken


def scan_index_files(check_anchors: bool = False) -> dict[str, list[str]]:
    """Scan index files only (default mode)."""
    all_broken: dict[str, list[str]] = {}
    scanned = 0

    index_files = [
        "README.md",
        "projects/index.md",
    ]
    for idx in index_files:
        p = AI_CONTEXT / idx
        if not p.exists():
            all_broken[idx] = ["MISSING"]
            continue
        broken = check_file(p, check_key_files=(idx == "projects/index.md"), check_anchors=check_anchors)
        scanned += 1
        if broken:
            all_broken[idx] = broken

    for proj_idx in sorted((AI_CONTEXT / "projects").rglob("*/index.md")):
        if is_project_index(proj_idx):
            broken = check_file(proj_idx, check_key_files=True, check_anchors=check_anchors)
            scanned += 1
            if broken:
                all_broken[str(proj_idx.relative_to(AI_CONTEXT))] = broken

    return all_broken


def format_human(all_broken: dict[str, list[str]], scanned: int, mode: str):
    """Human-readable output."""
    print(f"AI_CONTEXT link check")
    print(f"Scanned:     {scanned} files")
    print(f"Broken refs: {len(all_broken)} files")
    print(f"Mode:        {mode}")
    print()

    if not all_broken:
        print("All links valid.")
        return

    for fname, refs in sorted(all_broken.items()):
        print(f"  {fname}:")
        for ref in refs:
            print(f"    broken {ref}")
        print()

    total = sum(len(v) for v in all_broken.values())
    print(f"Total broken: {total}")


def format_json(all_broken: dict[str, list[str]], scanned: int, mode: str) -> str:
    """JSON output."""
    result = {
        "tool": "ai_context_link_check",
        "scanned": scanned,
        "broken_files": len(all_broken),
        "mode": mode,
        "issues": {k: v for k, v in all_broken.items()},
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    mode_flags = {
        "all": "--all" in sys.argv,
        "json": "--json" in sys.argv,
        "anchors": "--anchors" in sys.argv,
    }

    if mode_flags["all"]:
        all_broken = scan_all_files(check_anchors=mode_flags["anchors"])
        scanned = sum(1 for _ in AI_MEMORY_ROOT.glob("*.md"))
        scanned += sum(1 for _ in AI_CONTEXT.rglob("*.md")
                       if _.relative_to(AI_CONTEXT).parts[0] not in SKIP_DIRS
                       and not any(p.startswith(".") for p in _.relative_to(AI_CONTEXT).parts))
        mode = "all" + (" +anchors" if mode_flags["anchors"] else "")
    else:
        all_broken = scan_index_files(check_anchors=mode_flags["anchors"])
        scanned = len([1 for _ in all_broken.keys()])  # approximate
        # Recalculate properly
        scanned = 0
        for idx in ["README.md", "projects/index.md"]:
            if (AI_CONTEXT / idx).exists():
                scanned += 1
        scanned += sum(1 for _ in (AI_CONTEXT / "projects").rglob("*/index.md")
                       if is_project_index(_))
        mode = "index" + (" +anchors" if mode_flags["anchors"] else "")

    if mode_flags["json"]:
        print(format_json(all_broken, scanned, mode))
    else:
        format_human(all_broken, scanned, mode)

    total_broken = sum(len(v) for v in all_broken.values())
    return 1 if total_broken > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
