"""Fail closed if deprecated OpenAI Assistants API integration patterns appear in code/config.

This guard is intentionally scoped to executable/configuration surfaces rather than prose
research history. OpenAI's Assistants API shuts down on 2026-08-26; new integrations must
use the Responses API / Conversations API path instead.

Canonical effect: NONE.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

SCAN_ROOTS = (
    ".github",
    "components",
    "examples",
    "experiments",
    "research-labs",
    "scripts",
    "tests",
)

ROOT_GLOBS = (
    "pyproject.toml",
    "requirements*.txt",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "Dockerfile",
    "docker-compose*.yml",
    "docker-compose*.yaml",
)

TEXT_SUFFIXES = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".sh",
    ".ps1",
}

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("assistants_endpoint", re.compile(r"/v1/assistants(?:/|\b)", re.IGNORECASE)),
    ("assistants_sdk", re.compile(r"(?:client\.)?beta\.assistants\b", re.IGNORECASE)),
    ("assistants_create", re.compile(r"\bassistants\.create\s*\(", re.IGNORECASE)),
    ("assistants_beta_header", re.compile(r"assistants\s*=\s*v2", re.IGNORECASE)),
    ("legacy_threads_sdk", re.compile(r"(?:client\.)?beta\.threads\b", re.IGNORECASE)),
    ("legacy_threads_endpoint", re.compile(r"/v1/threads(?:/|\b)", re.IGNORECASE)),
)

SELF = Path(__file__).resolve()


def candidate_files(root: Path) -> list[Path]:
    found: set[Path] = set()
    for dirname in SCAN_ROOTS:
        base = root / dirname
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                found.add(path)
    for pattern in ROOT_GLOBS:
        for path in root.glob(pattern):
            if path.is_file():
                found.add(path)
    return sorted(found)


def audit(root: Path) -> dict[str, object]:
    matches: list[dict[str, object]] = []
    scanned = 0
    for path in candidate_files(root):
        if path.resolve() == SELF:
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, pattern in PATTERNS:
                if pattern.search(line):
                    matches.append(
                        {
                            "file": path.relative_to(root).as_posix(),
                            "line": line_no,
                            "pattern": label,
                            "snippet": line.strip()[:240],
                        }
                    )
    return {
        "status": "PASS" if not matches else "FAIL",
        "upstream_system": "OpenAI Assistants API",
        "shutdown_date": "2026-08-26",
        "recommended_replacement": "Responses API + Conversations API",
        "scanned_files": scanned,
        "matches": matches,
        "canonical_effect": "NONE",
    }


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    report = audit(root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
