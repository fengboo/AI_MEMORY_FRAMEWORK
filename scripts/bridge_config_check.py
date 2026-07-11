#!/usr/bin/env python3
"""Validate AI_MEMORY bridge switches and root references."""
from __future__ import annotations
import argparse, json, os, re
from pathlib import Path
from diagnostics import Diagnostic, SCHEMA_VERSION, should_fail, summary

REQUIRED = ("GLOBAL_WORKFLOW_RO", "MEMORY_POLICY_RO", "PROJECT_MEMORY_RO", "SKILLS_RO", "PROJECT_MEMORY_RW", "ROUTE_LOG_RW")
DEPS = {"PROJECT_MEMORY_RW": ("PROJECT_MEMORY_RO", "MEMORY_POLICY_RO"), "ROUTE_LOG_RW": ("PROJECT_MEMORY_RO",)}
ENV = (r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$", r"^\$([A-Za-z_][A-Za-z0-9_]*)$", r"^%([A-Za-z_][A-Za-z0-9_]*)%$", r"^env:([A-Za-z_][A-Za-z0-9_]*)$")

def switches(text: str) -> dict[str, str]:
    found = {m.group(1): m.group(2).lower() for m in re.finditer(r"<!--\s*(\w+)\s*=\s*([^\s]+)\s*-->", text)}
    return {key: value for key, value in found.items() if key in REQUIRED}

def root_value(text: str) -> str | None:
    match = re.search(r"<!--\s*AI_MEMORY_ROOT\s*=\s*(\S.*?)\s*-->", text)
    return match.group(1).strip() if match else None

def env_name(value: str) -> str | None:
    for pattern in ENV:
        match = re.match(pattern, value)
        if match: return match.group(1)
    return None

def check(path: Path, repo: Path, require_root: bool) -> list[Diagnostic]:
    rel = str(path.relative_to(repo)) if path.is_relative_to(repo) else str(path)
    if path.is_symlink():
        if path.exists(): return [Diagnostic("BR103", "info", f"symlink to {path.resolve().name}", rel)]
        return [Diagnostic("BR006", "error", "broken bridge symlink", rel)]
    try: text = path.read_text(encoding="utf-8")
    except OSError as exc: return [Diagnostic("BR007", "error", f"cannot read file: {exc}", rel)]
    if re.search(r"^status\s*:\s*deprecated\s*$", text, re.MULTILINE):
        return [Diagnostic("BR102", "info", "deprecated migration reference", rel)]
    parsed = switches(text); result: list[Diagnostic] = []
    if not parsed: return [Diagnostic("BR001", "error", "no bridge switches found", rel)]
    for key in REQUIRED:
        if key not in parsed: result.append(Diagnostic("BR001", "error", f"missing switch: {key}", rel))
    for key, value in parsed.items():
        if value not in {"on", "off"}: result.append(Diagnostic("BR002", "error", f"invalid switch value: {key}={value}", rel))
    for key, dependencies in DEPS.items():
        if parsed.get(key) == "on":
            for dependency in dependencies:
                if parsed.get(dependency) != "on": result.append(Diagnostic("BR003", "error", f"{key}=on requires {dependency}=on", rel))
    if require_root:
        value = root_value(text)
        if value is None: result.append(Diagnostic("BR004", "error", "AI_MEMORY_ROOT not found", rel))
        elif value in {"<AI_MEMORY_ROOT>", "/path/to/AI_MEMORY", "<path-to-AI_MEMORY>"}: result.append(Diagnostic("BR101", "info", "portable root placeholder", rel))
        else:
            name = env_name(value)
            if name:
                value = os.environ.get(name, "")
                if not value: result.append(Diagnostic("BR101", "info", f"environment root {name} is unresolved", rel))
            if value:
                candidate = Path(value)
                if not candidate.is_absolute(): candidate = path.parent / candidate
                if not candidate.is_dir(): result.append(Diagnostic("BR005", "error", f"AI_MEMORY_ROOT path does not exist: {value}", rel))
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?"); parser.add_argument("--all", action="store_true"); parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-root", action="store_true"); parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(); repo = args.root.resolve()
    if args.all and args.target: parser.error("use either target or --all")
    if not args.all and not args.target: parser.error("target or --all is required")
    paths = [repo / "templates" / "AGENTS.bridge.md", repo / "templates" / "CLAUDE.bridge.md"] if args.all else [Path(args.target).resolve()]
    diagnostics: list[Diagnostic] = []
    for path in paths:
        if not path.exists() and not path.is_symlink(): diagnostics.append(Diagnostic("BR007", "error", "bridge file not found", str(path)))
        else: diagnostics.extend(check(path, repo, args.require_root))
    payload = {"schema_version": SCHEMA_VERSION, "tool": "bridge_config_check", "mode": "all" if args.all else "single", "summary": summary(diagnostics, len(paths)), "diagnostics": [item.to_dict() for item in diagnostics]}
    if args.json: print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        counts = payload["summary"]; print(f"Bridge config check\nScanned: {len(paths)}\nErrors: {counts['errors']}  Warnings: {counts['warnings']}  Info: {counts['info']}")
        for item in diagnostics: print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")
    return 1 if should_fail(diagnostics, args.fail_on_warning) else 0
if __name__ == "__main__": raise SystemExit(main())
