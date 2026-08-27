from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_FILES = (
    "README.md",
    "README.zh-TW.md",
    "docs/START_HERE.md",
    "docs/CURRENT_STATE.md",
    "docs/INDEX.md",
    "docs/README.md",
    "docs/governance/DOCUMENTATION_GOVERNANCE.md",
)

REQUIRED_MARKERS = {
    "README.md": (
        "docs/START_HERE.md",
        "docs/CURRENT_STATE.md",
        "docs/INDEX.md",
        "SUBJECTIVITY = NOT_ESTABLISHED",
    ),
    "README.zh-TW.md": (
        "docs/START_HERE.md",
        "docs/CURRENT_STATE.md",
        "docs/INDEX.md",
        "SUBJECTIVITY = NOT_ESTABLISHED",
    ),
    "docs/START_HERE.md": (
        "AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION",
        "CURRENT_STATE.md",
        "INDEX.md",
        "FILE_COUNT != AUTHORITY",
    ),
    "docs/CURRENT_STATE.md": (
        "SCIENTIFIC_DISPOSITION = HOLD",
        "SUBJECTIVITY = NOT_ESTABLISHED",
        "CONSCIOUSNESS = NOT_ESTABLISHED",
        "INDEPENDENT_IVV = NOT_ACHIEVED",
        "STATIC_CURRENT_STATE != LIVE_CI_LEDGER",
    ),
    "docs/INDEX.md": (
        "CURRENT_ENTRY",
        "CURRENT_STATE",
        "HISTORICAL",
        "governance/DOCUMENTATION_GOVERNANCE.md",
    ),
    "docs/README.md": (
        "START_HERE.md",
        "CURRENT_STATE.md",
        "INDEX.md",
        "HISTORICAL_RECORD = PRESERVE_EVENT_TIME_MEANING",
    ),
    "docs/governance/DOCUMENTATION_GOVERNANCE.md": (
        "FILE_COUNT != AUTHORITY",
        "HISTORICAL_RECORD != CURRENT_STATE",
        "DOCUMENTATION_CONVERGENCE != RESEARCH_SCOPE_EXPANSION",
        "NEW_DOCUMENT_REQUIRES_DISTINCT_RESPONSIBILITY = TRUE",
    ),
}

FORBIDDEN_ENTRY_MARKERS = {
    "docs/README.md": (
        "Current documentation map after the 2026-08-18 indefinite repository freeze",
        "VISIBLE_BRANCH_COUNT = 2",
        "OPEN_PULL_REQUESTS = 0",
    ),
}

MAX_BYTES = {
    "README.md": 7000,
    "README.zh-TW.md": 8000,
    "docs/README.md": 5000,
    "docs/START_HERE.md": 9000,
    "docs/CURRENT_STATE.md": 10000,
}

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _local_markdown_links(path: Path, text: str) -> list[Path]:
    targets: list[Path] = []
    for raw in LINK_RE.findall(text):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required documentation entry file: {rel}")
            continue

        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED_MARKERS.get(rel, ()):
            if marker not in text:
                errors.append(f"{rel} is missing required marker: {marker}")

        for marker in FORBIDDEN_ENTRY_MARKERS.get(rel, ()):
            if marker in text:
                errors.append(f"{rel} retains stale entry-point marker: {marker}")

        byte_limit = MAX_BYTES.get(rel)
        if byte_limit is not None and len(text.encode("utf-8")) > byte_limit:
            errors.append(
                f"{rel} exceeds reader-entry size cap: "
                f"{len(text.encode('utf-8'))} > {byte_limit} bytes"
            )

        for target in _local_markdown_links(path, text):
            try:
                target.relative_to(root)
            except ValueError:
                errors.append(f"{rel} links outside repository: {target}")
                continue
            if not target.exists():
                errors.append(f"{rel} has missing local link target: {target.relative_to(root)}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate converged documentation entry points")
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Documentation entry and convergence checks: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
