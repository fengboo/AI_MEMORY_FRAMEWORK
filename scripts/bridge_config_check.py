"""Bridge config checker for AI_MEMORY bridge templates and project bridge files.

Validates that bridge switches are present, correctly spelled, have valid
values (on/off), and satisfy RW dependency rules.

Supports two config formats (checked in order):
  1. Fenced YAML block: ```yaml ... ``` with bridge_config key
  2. HTML comment format: <!-- SWITCH_NAME = on/off -->

Usage:
  python scripts/bridge_config_check.py <bridge_file>
  python scripts/bridge_config_check.py --all  # check all bridges under AI_MEMORY/

Options:
  --json          output results as JSON
  --require-root  require AI_MEMORY_ROOT to be a valid existing path
                  (off by default; template placeholders are accepted)
  --root <path>   set AI_MEMORY root (default: script parent directory)
"""

import sys
import re
import json
from pathlib import Path


def _find_root() -> Path:
    """Find AI_MEMORY root. Checks --root arg first, then script location."""
    for i, arg in enumerate(sys.argv):
        if arg == "--root" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1]).resolve()
    return Path(__file__).resolve().parent.parent


AI_MEMORY_ROOT = _find_root()

REQUIRED_SWITCHES = [
    "GLOBAL_WORKFLOW_RO",
    "MEMORY_POLICY_RO",
    "PROJECT_MEMORY_RO",
    "SKILLS_RO",
    "PROJECT_MEMORY_RW",
    "ROUTE_LOG_RW",
]

READ_SWITCHES = {
    "GLOBAL_WORKFLOW_RO",
    "MEMORY_POLICY_RO",
    "PROJECT_MEMORY_RO",
    "SKILLS_RO",
}

WRITE_SWITCHES = {
    "PROJECT_MEMORY_RW",
    "ROUTE_LOG_RW",
}

# (write_switch, depends_on_read)
RW_DEPENDENCIES = {
    "PROJECT_MEMORY_RW": ["PROJECT_MEMORY_RO", "MEMORY_POLICY_RO"],
    "ROUTE_LOG_RW": ["PROJECT_MEMORY_RO"],
}


def parse_html_comment_switches(text: str) -> dict[str, str]:
    """Parse switches from HTML comment lines: <!-- NAME = value -->"""
    switches = {}
    for m in re.finditer(r"<!--\s*(\w+)\s*=\s*(on|off)\s*-->", text, re.IGNORECASE):
        name = m.group(1)
        value = m.group(2).lower()
        if name in REQUIRED_SWITCHES:
            switches[name] = value
    return switches


def extract_root_path(text: str) -> str | None:
    """Extract AI_MEMORY_ROOT value from HTML comment or YAML.

    Matches:
      <!-- AI_MEMORY_ROOT = <value> -->
      AI_MEMORY_ROOT: <value>  (in YAML block)
    """
    # HTML comment format
    m = re.search(r"<!--\s*AI_MEMORY_ROOT\s*=\s*(\S[^\n]*?)\s*-->", text)
    if m:
        return m.group(1).strip()
    # YAML fenced block format
    m = re.search(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            stripped = line.strip()
            if stripped.startswith("AI_MEMORY_ROOT:") or stripped.startswith("AI_MEMORY_ROOT ="):
                _, _, val = stripped.partition(":")
                if not val:
                    _, _, val = stripped.partition("=")
                return val.strip()
    return None


PLACEHOLDER_PATTERNS = [
    r"^<AI_MEMORY_ROOT>$",
    r"^/path/to/AI_MEMORY$",
    r"^<path-to-AI_MEMORY>$",
    r"^\$AI_MEMORY_ROOT$",
    r"^\$\{AI_MEMORY_ROOT\}$",
]


def is_placeholder(path_str: str) -> bool:
    """Check if a path string is a recognized placeholder."""
    for pat in PLACEHOLDER_PATTERNS:
        if re.match(pat, path_str):
            return True
    return False


def check_root_path(file_path: Path, root_value: str) -> list[str]:
    """Validate that AI_MEMORY_ROOT points to an existing directory.

    Returns empty list (pass) or list of issue strings.
    Placeholder values are accepted (not errors).
    """
    if is_placeholder(root_value):
        return []

    candidate = Path(root_value)
    if not candidate.is_absolute():
        # Resolve relative to the bridge file location
        candidate = (file_path.parent / root_value).resolve()

    if candidate.is_dir():
        return []

    return [f"AI_MEMORY_ROOT path does not exist: {root_value}"]


def parse_fenced_yaml_switches(text: str) -> dict[str, str] | None:
    """Try to extract a fenced YAML bridge config block."""
    m = re.search(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    if not m:
        return None
    switches = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().lower()
            if key in REQUIRED_SWITCHES:
                switches[key] = val
    return switches if switches else None


def check_bridge(file_path: Path, require_root: bool = False) -> list[str]:
    """Return list of issues for a bridge file.

    If require_root is True, also validate that AI_MEMORY_ROOT points
    to an existing directory (template placeholders are accepted).
    """
    issues = []

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read file: {e}"]

    # Try fenced YAML first, then HTML comments
    switches = parse_fenced_yaml_switches(text)
    if switches is None:
        switches = parse_html_comment_switches(text)

    if not switches:
        issues.append("no bridge switches found (tried YAML fenced block and HTML comments)")
        return issues

    # Check all required switches present
    for sw in REQUIRED_SWITCHES:
        if sw not in switches:
            issues.append(f"missing switch: {sw}")

    # Check values
    for name, value in switches.items():
        if name in REQUIRED_SWITCHES and value not in ("on", "off"):
            issues.append(f"invalid value for {name}: '{value}' (must be on/off)")

    # Check RW dependencies
    for rw_sw, deps in RW_DEPENDENCIES.items():
        if switches.get(rw_sw) == "on":
            for dep in deps:
                if switches.get(dep) != "on":
                    issues.append(
                        f"dependency violation: {rw_sw}=on requires {dep}=on, "
                        f"but {dep}={switches.get(dep, 'missing')}"
                    )

    # --require-root: validate AI_MEMORY_ROOT path
    if require_root:
        root_value = extract_root_path(text)
        if root_value is None:
            issues.append("AI_MEMORY_ROOT not found in bridge file (required by --require-root)")
        else:
            root_issues = check_root_path(file_path, root_value)
            issues.extend(root_issues)

    return issues


def scan_all_bridges(require_root: bool = False) -> dict[str, list[str]]:
    """Find and check all bridge files under AI_MEMORY."""
    results = {}
    candidates = [
        AI_MEMORY_ROOT / "templates" / "AGENTS.bridge.md",
        AI_MEMORY_ROOT / "templates" / "CLAUDE.bridge.md",
    ]
    for p in candidates:
        if p.exists():
            issues = check_bridge(p, require_root=require_root)
            if issues:
                results[str(p.relative_to(AI_MEMORY_ROOT))] = issues
    return results


def format_human(all_issues: dict[str, list[str]], mode: str):
    """Human-readable output."""
    print(f"Bridge config check")
    print(f"Mode:        {mode}")
    print(f"Files with issues: {len(all_issues)}")
    print()

    if not all_issues:
        print("All bridge configs valid.")
        return

    for fname, issues in sorted(all_issues.items()):
        print(f"  {fname}:")
        for issue in issues:
            print(f"    - {issue}")
        print()

    total = sum(len(v) for v in all_issues.values())
    print(f"Total issues: {total}")


def format_json(all_issues: dict[str, list[str]], mode: str) -> str:
    """JSON output."""
    result = {
        "tool": "bridge_config_check",
        "mode": mode,
        "files_with_issues": len(all_issues),
        "issues": {k: v for k, v in all_issues.items()},
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    use_json = "--json" in sys.argv
    use_all = "--all" in sys.argv
    require_root = "--require-root" in sys.argv

    if use_all:
        all_issues = scan_all_bridges(require_root=require_root)
        mode = "all" + (" +require-root" if require_root else "")
    else:
        # Find the first non-flag argument as the bridge file path
        target = None
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                target = arg
                break

        if not target:
            print("Usage: python scripts/bridge_config_check.py <bridge_file> [--all] [--json] [--require-root]",
                  file=sys.stderr)
            return 2

        bridge_path = Path(target)
        if not bridge_path.is_absolute():
            bridge_path = (Path.cwd() / bridge_path).resolve()

        if not bridge_path.exists():
            print(f"File not found: {bridge_path}", file=sys.stderr)
            return 1

        issues = check_bridge(bridge_path, require_root=require_root)
        rel = bridge_path.relative_to(AI_MEMORY_ROOT) if bridge_path.is_relative_to(AI_MEMORY_ROOT) else str(bridge_path)
        all_issues = {rel: issues} if issues else {}
        mode = "single" + (" +require-root" if require_root else "")

    if use_json:
        print(format_json(all_issues, mode))
    else:
        format_human(all_issues, mode)

    total = sum(len(v) for v in all_issues.values())
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
