"""Shared diagnostic helpers for repository validation commands."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Literal


Severity = Literal["error", "warning", "info"]
SCHEMA_VERSION = 1


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    path: str | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def summary(diagnostics: Iterable[Diagnostic], scanned: int = 0) -> dict[str, int]:
    result = {"scanned": scanned, "errors": 0, "warnings": 0, "info": 0}
    for diagnostic in diagnostics:
        key = "info" if diagnostic.severity == "info" else f"{diagnostic.severity}s"
        result[key] += 1
    return result


def should_fail(diagnostics: Iterable[Diagnostic], fail_on_warning: bool = False) -> bool:
    return any(
        diagnostic.severity == "error"
        or (fail_on_warning and diagnostic.severity == "warning")
        for diagnostic in diagnostics
    )
