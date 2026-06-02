#!/usr/bin/env python3
"""
Future stub: lifecycle_metadata_lint.py

Purpose:
    Validate optional lifecycle metadata when present.

Current phase:
    This script is non-blocking and informational.
    It should not be added as a strict CI requirement yet.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
AI_CONTEXT = ROOT / "AI_CONTEXT"

VALID_LIFECYCLE = {
    "active", "warm", "cold", "archived", "deprecated", "superseded", "deleted"
}

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

    warnings = []

    for path in sorted(AI_CONTEXT.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_front_matter(text)
        lifecycle = fm.get("lifecycle")
        if lifecycle and lifecycle not in VALID_LIFECYCLE:
            warnings.append((path, f"invalid lifecycle: {lifecycle}"))

    if not warnings:
        print("No lifecycle metadata warnings.")
        return 0

    print("Lifecycle metadata warnings:")
    for path, msg in warnings:
        print(f"- {path.relative_to(ROOT)}: {msg}")

    print()
    print("Note: warnings are informational only in current phase.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
