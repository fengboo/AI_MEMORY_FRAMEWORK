#!/usr/bin/env python3
"""Install or merge AI_MEMORY bridge rules into AGENTS.md / CLAUDE.md."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


BEGIN = "<!-- BEGIN AI_MEMORY_BRIDGE -->"
END = "<!-- END AI_MEMORY_BRIDGE -->"

SWITCHES = [
    "GLOBAL_WORKFLOW_RO",
    "MEMORY_POLICY_RO",
    "PROJECT_MEMORY_RO",
    "SKILLS_RO",
    "PROJECT_MEMORY_RW",
    "ROUTE_LOG_RW",
]

MODES = {
    "small": {
        "GLOBAL_WORKFLOW_RO": "on",
        "MEMORY_POLICY_RO": "off",
        "PROJECT_MEMORY_RO": "off",
        "SKILLS_RO": "off",
        "PROJECT_MEMORY_RW": "off",
        "ROUTE_LOG_RW": "off",
    },
    "medium": {
        "GLOBAL_WORKFLOW_RO": "on",
        "MEMORY_POLICY_RO": "off",
        "PROJECT_MEMORY_RO": "on",
        "SKILLS_RO": "on",
        "PROJECT_MEMORY_RW": "off",
        "ROUTE_LOG_RW": "off",
    },
    "large": {
        "GLOBAL_WORKFLOW_RO": "on",
        "MEMORY_POLICY_RO": "on",
        "PROJECT_MEMORY_RO": "on",
        "SKILLS_RO": "on",
        "PROJECT_MEMORY_RW": "on",
        "ROUTE_LOG_RW": "on",
    },
}


def find_ai_memory_root() -> Path:
    env = os.environ.get("AI_MEMORY_ROOT")
    if env:
        root = Path(env).expanduser().resolve()
        if (root / "templates").is_dir():
            return root
        raise SystemExit(f"AI_MEMORY_ROOT does not contain templates/: {root}")

    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "templates").is_dir() and (parent / "AI_CONTEXT").is_dir():
            return parent

    raise SystemExit("AI_MEMORY_ROOT is not set and AI_MEMORY repo root was not found")


def template_name(agent: str) -> tuple[str, str]:
    if agent == "codex":
        return "AGENTS.md", "AGENTS.bridge.md"
    if agent == "claude":
        return "AGENTS.md", "AGENTS.bridge.md"
    raise SystemExit(f"Unsupported agent: {agent}")


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    return text[end + len("\n---") :].lstrip()


def demote_headings(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            lines.append("#" + line)
        else:
            lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def bridge_section(template_text: str, mode: str) -> str:
    body = strip_frontmatter(template_text)
    body_lines = body.splitlines()
    if body_lines and body_lines[0].startswith("# "):
        body = "\n".join(body_lines[1:]).lstrip()
    body = apply_mode(body, mode)
    body = demote_headings(body)
    return f"{BEGIN}\n## AI_MEMORY Bridge\n\n{body}{END}\n"


def apply_mode(text: str, mode: str) -> str:
    if mode == "template":
        return text
    values = MODES[mode]
    for switch in SWITCHES:
        value = values[switch]
        text = re.sub(
            rf"<!--\s*{switch}\s*=\s*(on|off)\s*-->",
            f"<!-- {switch}  = {value} -->",
            text,
        )
    return text


def replace_marked_block(existing: str, section: str) -> tuple[str, str]:
    pattern = re.compile(
        rf"{re.escape(BEGIN)}.*?{re.escape(END)}\n?",
        flags=re.DOTALL,
    )
    if pattern.search(existing):
        return pattern.sub(section, existing), "updated existing marked AI_MEMORY Bridge block"

    heading = re.search(r"(?m)^## AI_MEMORY Bridge\s*$", existing)
    if heading:
        start = heading.start()
        next_heading = re.search(r"(?m)^## (?!AI_MEMORY Bridge\b).*$", existing[heading.end() :])
        if next_heading:
            end = heading.end() + next_heading.start()
            merged = existing[:start].rstrip() + "\n\n" + section + "\n" + existing[end:].lstrip()
        else:
            merged = existing[:start].rstrip() + "\n\n" + section
        return merged.rstrip() + "\n", "replaced existing AI_MEMORY Bridge section"

    merged = existing.rstrip() + "\n\n" + section
    return merged.rstrip() + "\n", "appended AI_MEMORY Bridge section"


def install_bridge(target_dir: Path, agent: str, mode: str, dry_run: bool) -> int:
    ai_memory_root = find_ai_memory_root()
    target_name, tmpl_name = template_name(agent)
    template_path = ai_memory_root / "templates" / tmpl_name
    target_file = target_dir / target_name

    if not template_path.exists():
        raise SystemExit(f"Missing template: {template_path}")
    if not target_dir.is_dir():
        raise SystemExit(f"Target directory does not exist: {target_dir}")

    template_text = template_path.read_text(encoding="utf-8")

    if target_file.exists():
        section = bridge_section(template_text, mode)
        existing = target_file.read_text(encoding="utf-8")
        new_text, action = replace_marked_block(existing, section)
    else:
        new_text = apply_mode(template_text, mode)
        action = "created new bridge file from template"

    if dry_run:
        print(f"DRY RUN: would write {target_file}")
        print(f"Action: {action}")
        if agent == "claude":
            print("DRY RUN: would ensure CLAUDE.md -> AGENTS.md symlink when safe")
        return 0

    target_file.write_text(new_text, encoding="utf-8")
    print(f"Wrote: {target_file}")
    print(f"Action: {action}")
    print(f"AI_MEMORY_ROOT: {ai_memory_root}")
    if agent == "claude":
        ensure_claude_symlink(target_dir)
    return 0


def ensure_claude_symlink(target_dir: Path) -> None:
    claude = target_dir / "CLAUDE.md"
    agents = target_dir / "AGENTS.md"
    if claude.is_symlink():
        target = os.readlink(claude)
        if target == "AGENTS.md":
            print("CLAUDE.md already symlinks to AGENTS.md")
        else:
            print(f"WARNING: CLAUDE.md is a symlink to {target}; left unchanged")
        return

    if claude.exists():
        print("WARNING: CLAUDE.md already exists as a standalone file; left unchanged")
        print("Merge its local rules into AGENTS.md before replacing it with a symlink.")
        return

    try:
        claude.symlink_to(agents.name)
        print("Created symlink: CLAUDE.md -> AGENTS.md")
    except OSError as exc:
        print(f"WARNING: could not create CLAUDE.md symlink: {exc}")
        print("Create the symlink manually or copy AGENTS.md to CLAUDE.md if symlinks are unavailable.")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Target project directory")
    parser.add_argument("--agent", choices=["codex", "claude"], required=True)
    parser.add_argument("--mode", choices=["template", "small", "medium", "large"], default="template")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    target = Path(args.target).expanduser().resolve()
    return install_bridge(target, args.agent, args.mode, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
