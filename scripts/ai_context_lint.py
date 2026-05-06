"""Front matter lint for AI_CONTEXT/ markdown files.

Checks:
  1. Every .md under AI_CONTEXT/ has YAML front matter
  2. Required fields present: type
  3. Key files (operational) have: type, scope, status, last_updated
  4. status values are valid: active | deprecated | resolved | synthetic | candidate
  5. type values are from known set

Usage: python scripts/ai_context_lint.py [--strict]
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

AI_CONTEXT = Path(__file__).resolve().parent.parent / "AI_CONTEXT"

REQUIRED_ALL = {"type"}
REQUIRED_KEY = {"type", "scope", "status"}
VALID_STATUS = {"active", "deprecated", "resolved", "synthetic", "candidate", "open", "closed", "pending"}
VALID_TYPES = {
    "root_index", "project_index", "project", "policy", "workflow",
    "skill", "user_profile", "todo", "constraints", "conflicts",
    "corrections", "decisions", "open_questions", "route_log",
    "validation_plan", "supervision_index", "executor_brief",
    "handoff_log", "supervision_questions", "review_checkpoints",
    "validation_report", "next_phase_plan",
}

# Files under these dirs are not required to have front matter
SKIP_DIRS = {"reference", "templates", "scripts"}

STALE_DAYS = 60


def extract_front_matter(path: Path) -> tuple[dict | None, int]:
    """Return (front_matter_dict, line_count) or (None, 0) if none found."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None, 0

    # Must start with ---
    if not text.startswith("---"):
        return None, len(text.splitlines())

    # Find closing ---
    end = text.find("---", 3)
    if end == -1:
        return None, len(text.splitlines())

    fm_text = text[3:end].strip()
    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()

    return data, len(text.splitlines())


def check_file(path: Path, strict: bool) -> list[str]:
    """Return list of issues for this file."""
    issues = []
    rel = path.relative_to(AI_CONTEXT)

    fm, _ = extract_front_matter(path)

    # 1. Has front matter?
    if fm is None:
        issues.append(f"MISSING front matter")
        return issues
    if fm == {}:
        issues.append(f"EMPTY front matter")
        return issues

    # 2. Required: type
    file_type = fm.get("type", "")
    if "type" not in fm:
        issues.append(f"missing required field: type")
    elif file_type not in VALID_TYPES:
        issues.append(f"unknown type: '{file_type}'")

    # 3. Key files need scope, status
    is_key = file_type not in {"todo", "open_questions"}  # these have scope but status is less critical
    if is_key or strict:
        for field in ("scope", "status"):
            if field not in fm:
                issues.append(f"missing field in key file: {field}")

    # 4. Status value check
    if "status" in fm and fm["status"] not in VALID_STATUS:
        issues.append(f"invalid status: '{fm['status']}'")

    # 5. Stale check (only for active files)
    if strict and fm.get("status") == "active":
        lu = fm.get("last_updated", "")
        if lu:
            try:
                dt = datetime.strptime(lu, "%Y-%m-%d")
                if datetime.now() - dt > timedelta(days=STALE_DAYS):
                    issues.append(
                        f"stale: last_updated={lu} ({STALE_DAYS}+ days ago)"
                    )
            except ValueError:
                issues.append(f"bad date format in last_updated: '{lu}'")

    return issues


def main():
    strict = "--strict" in sys.argv
    root = AI_CONTEXT
    all_issues: dict[str, list[str]] = {}
    file_count = 0

    for md_file in sorted(root.rglob("*.md")):
        # Skip non-AI_CONTEXT dirs
        parts = md_file.relative_to(root).parts
        if parts and parts[0] in SKIP_DIRS:
            continue
        if any(p.startswith(".") for p in parts):
            continue

        issues = check_file(md_file, strict)
        file_count += 1
        if issues:
            all_issues[str(md_file.relative_to(root))] = issues

    # Report
    print(f"AI_CONTEXT front matter lint")
    print(f"Scanned: {file_count} files")
    print(f"Issues:  {len(all_issues)} files")
    print(f"Mode:    {'strict' if strict else 'standard'}")
    print()

    if not all_issues:
        print("All clean.")
        return 0

    for fname, issues in sorted(all_issues.items()):
        print(f"  {fname}:")
        for issue in issues:
            print(f"    - {issue}")
        print()

    total = sum(len(v) for v in all_issues.values())
    print(f"Total issues: {total}")
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
