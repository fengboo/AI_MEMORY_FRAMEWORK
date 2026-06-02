"""Front matter lint for AI_CONTEXT/ markdown files.

Checks:
  1. Every .md under AI_CONTEXT/ has YAML front matter
  2. Required fields present: type
  3. Key files (operational) have: type, scope, status, last_updated
  4. status values are valid: active | deprecated | resolved | synthetic | candidate | ...
  5. type values are from known set

Options:
  --strict : also check stale dates (last_updated > 60 days) and enforce
             last_updated on key files
  --json   : output results as JSON (default: human-readable)

Usage: python scripts/ai_context_lint.py [--strict] [--json] [--root <path>]
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime, timedelta


def _find_root() -> Path:
    """Find AI_MEMORY root. Checks --root arg first, then script location."""
    for i, arg in enumerate(sys.argv):
        if arg == "--root" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1]).resolve()
    return Path(__file__).resolve().parent.parent


AI_MEMORY_ROOT = _find_root()
AI_CONTEXT = AI_MEMORY_ROOT / "AI_CONTEXT"

REQUIRED_ALL = {"type"}
# Key files must have type, scope, status. last_updated enforced in --strict mode.
REQUIRED_KEY = {"type", "scope", "status"}
VALID_STATUS = {"active", "deprecated", "resolved", "synthetic", "candidate",
                "open", "closed", "pending", "draft"}
VALID_TYPES = {
    "root_index", "project_index", "project", "policy", "workflow",
    "skill", "user_profile", "todo", "constraints", "conflicts",
    "corrections", "decisions", "open_questions", "route_log",
    "validation_plan", "supervision_index", "executor_brief",
    "handoff_log", "supervision_questions", "review_checkpoints",
    "validation_report", "next_phase_plan", "index", "flow", "tool",
    "pattern", "convention",
}

SKIP_DIRS = {"reference", "templates", "scripts"}

STALE_DAYS = 60


def extract_front_matter(path: Path) -> tuple[dict | None, int]:
    """Return (front_matter_dict, line_count) or (None, 0) if none found.

    Requires the opening --- to be on line 1 and closing --- on its own line.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None, 0

    lines = text.splitlines()

    # Must start with ---
    if not lines or lines[0].strip() != "---":
        return None, len(lines)

    # Find closing --- on its own line
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, len(lines)

    fm_text = "\n".join(lines[1:end_idx]).strip()
    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()

    return data, len(lines)


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

    # 3. Key files need scope, status, and last_updated (enforced in strict)
    is_key = file_type not in {"todo", "open_questions"}
    if is_key or strict:
        for field in REQUIRED_KEY:
            if field not in fm:
                issues.append(f"missing field in key file: {field}")
        if strict and "last_updated" not in fm:
            issues.append(f"missing field in key file: last_updated (required in --strict)")

    # 4. Status value check
    if "status" in fm and fm["status"] not in VALID_STATUS:
        issues.append(f"invalid status: '{fm['status']}'")

    # 5. Stale check — only in --strict mode
    # The health-check in memory_policy.md expects stale detection to be run
    # periodically.  The --strict flag is the canonical path for this check;
    # without it, stale detection is skipped.
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


def format_human(all_issues: dict[str, list[str]], file_count: int, mode: str):
    """Human-readable output."""
    print(f"AI_CONTEXT front matter lint")
    print(f"Scanned: {file_count} files")
    print(f"Issues:  {len(all_issues)} files")
    print(f"Mode:    {mode}")
    print()

    if not all_issues:
        print("All clean.")
        return

    for fname, issues in sorted(all_issues.items()):
        print(f"  {fname}:")
        for issue in issues:
            print(f"    - {issue}")
        print()

    total = sum(len(v) for v in all_issues.values())
    print(f"Total issues: {total}")


def format_json(all_issues: dict[str, list[str]], file_count: int, mode: str) -> str:
    """JSON output."""
    result = {
        "tool": "ai_context_lint",
        "scanned": file_count,
        "files_with_issues": len(all_issues),
        "mode": mode,
        "issues": {k: v for k, v in all_issues.items()},
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    strict = "--strict" in sys.argv
    use_json = "--json" in sys.argv
    mode = "strict" if strict else "standard"

    root = AI_CONTEXT
    all_issues: dict[str, list[str]] = {}
    file_count = 0

    for md_file in sorted(root.rglob("*.md")):
        parts = md_file.relative_to(root).parts
        if parts and parts[0] in SKIP_DIRS:
            continue
        if any(p.startswith(".") for p in parts):
            continue

        issues = check_file(md_file, strict)
        file_count += 1
        if issues:
            all_issues[str(md_file.relative_to(root))] = issues

    if use_json:
        print(format_json(all_issues, file_count, mode))
    else:
        format_human(all_issues, file_count, mode)

    total = sum(len(v) for v in all_issues.values())
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
