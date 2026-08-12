from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache", "coverage"}
FORBIDDEN_SUFFIXES = {".zip", ".whl", ".sqlite3", ".db", ".pyc", ".coverage"}
PATTERNS = {
    "windows_private_path": re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s]+", re.IGNORECASE),
    "unix_private_path": re.compile(r"/home/(?:[^/\s]+)/(?:upload|Downloads|Desktop|Documents)(?:/|\\s|$)", re.IGNORECASE),
    "credential_assignment": re.compile(r"(?:api[_-]?key|access[_-]?token|secret|password)\\s*[:=]\\s*['\"][^'\"]+['\"]", re.IGNORECASE),
}
errors: list[str] = []
scanned = 0
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        continue
    scanned += 1
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        errors.append(f"forbidden artifact suffix: {relative}")
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        errors.append(f"non-UTF8 or unreadable file: {relative}")
        continue
    for name, pattern in PATTERNS.items():
        if pattern.search(text):
            # The public redaction implementation necessarily contains a regex
            # describing a Windows path. It is policy code, not owner data; the
            # literal replacement marker is the explicit, narrow exception.
            if name == "windows_private_path" and "[REDACTED_USER]" in text and "C:\\\\Users\\\\[REDACTED_USER]" in text:
                continue
            errors.append(f"{name}: {relative}")

result = {"status": "PASS" if not errors else "FAIL", "scope": "CURRENT_AION_REPOSITORY_TREE", "scanned_files": scanned, "errors": errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
