"""Link checker for AI_CONTEXT/ internal references.

Checks that:
  1. [text](path) markdown links point to existing files
  2. Project index "Key Files" entries exist relative to the project directory

Usage: python scripts/ai_context_link_check.py
"""

import re
import sys
from pathlib import Path

AI_CONTEXT = Path(__file__).resolve().parent.parent / "AI_CONTEXT"


def extract_md_links(text: str) -> list[tuple[str, str]]:
    """Extract (path, context_hint) from [text](path) markdown links."""
    results = []
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        path = m.group(2).strip()
        # Skip URLs and anchors
        if not path or path.startswith(("http://", "https://", "#")):
            continue
        path = path.split("#")[0]
        results.append((path, "link"))
    return results


def extract_key_files(text: str) -> list[str]:
    """Extract filenames from Key Files / 关键文件 section in project index.

    Matches lines like:
      - `decisions.md` — description
      - `supervision/` — description

    Results are verified as actual files in check_file().
    """
    results = []
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()

        # Detect section heading
        if re.search(r"(Key Files|关键文件)", stripped):
            in_section = True
            continue

        if not in_section:
            continue

        # Exit on next heading
        if stripped.startswith("##"):
            in_section = False
            continue

        # Collect list items: - `filename.md` or - filename.md
        # Also match directory refs like `supervision/`
        m = re.match(r"-\s+`([^`]+)`", stripped)
        if m:
            ref = m.group(1)
            if ref.endswith((".md", "/")):
                results.append(ref)
            continue

        # Also match bare filenames after -:  - decisions.md
        m = re.match(r"-\s+([\w\-/]+\.md)", stripped)
        if m:
            results.append(m.group(1))
            continue

        # Stop at next non-list-item, non-blank line
        if stripped and not stripped.startswith("- "):
            in_section = False

    return results


def resolve(path: Path, ref: str) -> Path | None:
    """Resolve a reference. Returns existing Path or None."""
    candidate = (path.parent / ref).resolve()
    if candidate.exists():
        return candidate
    candidate = (AI_CONTEXT / ref).resolve()
    if candidate.exists():
        return candidate
    return None


def check_file(path: Path) -> list[str]:
    """Return broken references for this file."""
    broken = []
    text = path.read_text(encoding="utf-8")
    is_project_index = path.parent.name != "projects" and path.name == "index.md"

    # Check [text](path) links
    for ref, ctx in extract_md_links(text):
        if not resolve(path, ref):
            broken.append(f"[link] → {ref}")

    # For project index.md, check Key Files section
    if is_project_index:
        for ref in extract_key_files(text):
            # Resolve relative to the project directory
            candidate = path.parent / ref
            if not candidate.exists():
                broken.append(f"[key file] → {ref}")

    return broken


def main():
    all_broken: dict[str, list[str]] = {}
    scanned = 0

    # Scan index files
    index_files = [
        "README.md",
        "projects/index.md",
    ]
    for idx in index_files:
        p = AI_CONTEXT / idx
        if not p.exists():
            print(f"MISSING: {idx}")
            continue
        broken = check_file(p)
        scanned += 1
        if broken:
            all_broken[idx] = broken

    # Scan project index.md files
    for proj_idx in sorted((AI_CONTEXT / "projects").rglob("*/index.md")):
        broken = check_file(proj_idx)
        scanned += 1
        if broken:
            all_broken[str(proj_idx.relative_to(AI_CONTEXT))] = broken

    print(f"AI_CONTEXT link check")
    print(f"Scanned:     {scanned} index files")
    print(f"Broken refs: {len(all_broken)} files")
    print()

    if not all_broken:
        print("All links valid.")
        return 0

    for fname, refs in sorted(all_broken.items()):
        print(f"  {fname}:")
        for ref in refs:
            print(f"    broken {ref}")
        print()

    total = sum(len(v) for v in all_broken.values())
    print(f"Total broken: {total}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
