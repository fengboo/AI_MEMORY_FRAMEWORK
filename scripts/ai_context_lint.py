#!/usr/bin/env python3
"""Validate YAML front matter under AI_CONTEXT/."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

from diagnostics import Diagnostic, SCHEMA_VERSION, should_fail, summary

REQUIRED_KEY = {"type", "scope", "status"}
VALID_STATUS = {"active", "deprecated", "resolved", "synthetic", "candidate", "open", "closed", "pending", "draft"}
VALID_TYPES = {"root_index", "project_index", "project", "policy", "workflow", "skill", "user_profile", "todo", "constraints", "conflicts", "corrections", "decisions", "open_questions", "route_log", "validation_plan", "supervision_index", "executor_brief", "handoff_log", "supervision_questions", "review_checkpoints", "validation_report", "next_phase_plan", "index", "flow", "tool", "pattern", "convention"}
SKIP_DIRS = {"reference", "templates", "scripts"}


def extract_front_matter(path: Path) -> dict[str, str] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return None
    values: dict[str, str] = {}
    for line in lines[1:end]:
        stripped = line.strip()
        if ":" in stripped and not stripped.startswith("#"):
            key, _, value = stripped.partition(":")
            values[key.strip()] = value.strip()
    return values


def check_file(path: Path, context: Path, strict: bool, stale_days: int) -> list[Diagnostic]:
    rel = path.relative_to(context).as_posix()
    fm = extract_front_matter(path)
    if fm is None:
        return [Diagnostic("FM001", "error", "missing front matter", rel)]
    if not fm:
        return [Diagnostic("FM001", "error", "empty front matter", rel)]
    diagnostics: list[Diagnostic] = []
    file_type = fm.get("type")
    if not file_type:
        diagnostics.append(Diagnostic("FM002", "error", "missing required field: type", rel))
    elif file_type not in VALID_TYPES:
        diagnostics.append(Diagnostic("FM003", "error", f"unknown type: {file_type!r}", rel))
    is_key = file_type not in {"todo", "open_questions"}
    if is_key or strict:
        for field in sorted(REQUIRED_KEY):
            if not fm.get(field):
                diagnostics.append(Diagnostic("FM002", "error", f"missing field in key file: {field}", rel))
        if strict and "last_updated" not in fm:
            diagnostics.append(Diagnostic("FM002", "error", "missing field in key file: last_updated", rel))
    if fm.get("status") and fm["status"] not in VALID_STATUS:
        diagnostics.append(Diagnostic("FM004", "error", f"invalid status: {fm['status']!r}", rel))
    if not fm.get("schema_version"):
        diagnostics.append(Diagnostic("FM100", "info", "legacy metadata without schema_version", rel))
    if strict and fm.get("status") == "active" and fm.get("last_updated"):
        try:
            updated = datetime.strptime(fm["last_updated"], "%Y-%m-%d")
        except ValueError:
            diagnostics.append(Diagnostic("FM005", "error", f"invalid last_updated date: {fm['last_updated']!r}", rel))
        else:
            if datetime.now() - updated > timedelta(days=stale_days):
                diagnostics.append(Diagnostic("FM101", "warning", f"stale active memory: last_updated={fm['last_updated']}", rel))
    return diagnostics


def format_human(diagnostics: list[Diagnostic], scanned: int) -> None:
    counts = summary(diagnostics, scanned)
    print(f"AI_CONTEXT front matter lint\nScanned: {scanned}\nErrors: {counts['errors']}  Warnings: {counts['warnings']}  Info: {counts['info']}")
    for item in diagnostics:
        print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="enable stale-date checks")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--stale-days", type=int, default=60)
    args = parser.parse_args()
    if args.stale_days <= 0:
        parser.error("--stale-days must be positive")
    context = args.root.resolve() / "AI_CONTEXT"
    diagnostics: list[Diagnostic] = []
    scanned = 0
    if not context.is_dir():
        diagnostics.append(Diagnostic("FM006", "error", "missing AI_CONTEXT directory", str(context)))
    else:
        for path in sorted(context.rglob("*.md")):
            parts = path.relative_to(context).parts
            if parts[0] in SKIP_DIRS or any(part.startswith(".") for part in parts):
                continue
            scanned += 1
            diagnostics.extend(check_file(path, context, args.strict, args.stale_days))
    payload = {"schema_version": SCHEMA_VERSION, "tool": "ai_context_lint", "mode": "strict" if args.strict else "standard", "summary": summary(diagnostics, scanned), "diagnostics": [item.to_dict() for item in diagnostics]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        format_human(diagnostics, scanned)
    return 1 if should_fail(diagnostics, args.fail_on_warning) else 0


if __name__ == "__main__":
    raise SystemExit(main())
