#!/usr/bin/env python3
"""
Future stub: memory_health.py

Purpose:
    Read-only placeholder for future memory lifecycle health checks.

Current behavior:
    - Scans Markdown files.
    - Counts files.
    - Detects optional lifecycle metadata when present.
    - Does not modify anything.

Future behavior:
    - stale memory detection
    - duplicate candidate detection
    - promote candidate detection
    - archive candidate detection
    - review queue generation
"""

from __future__ import annotations

from pathlib import Path
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
AI_CONTEXT = ROOT / "AI_CONTEXT"

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}
    data: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> int:
    if not AI_CONTEXT.exists():
        print(f"AI_CONTEXT not found: {AI_CONTEXT}")
        return 1

    md_files = sorted(AI_CONTEXT.rglob("*.md"))
    lifecycle_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    missing_lifecycle = 0

    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_front_matter(text)
        lifecycle = fm.get("lifecycle")
        mem_type = fm.get("type")
        if lifecycle:
            lifecycle_counts[lifecycle] += 1
        else:
            missing_lifecycle += 1
        if mem_type:
            type_counts[mem_type] += 1

    print("Memory Health Stub Report")
    print("=========================")
    print(f"Markdown files: {len(md_files)}")
    print(f"Files without lifecycle metadata: {missing_lifecycle}")
    print()
    print("Lifecycle counts:")
    for key, count in lifecycle_counts.most_common():
        print(f"  {key}: {count}")
    print()
    print("Type counts:")
    for key, count in type_counts.most_common():
        print(f"  {key}: {count}")

    print()
    print("Note: This is a read-only future stub. It does not modify files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
