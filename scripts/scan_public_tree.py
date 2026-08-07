from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROHIBITED_SUFFIXES = {".zip", ".whl", ".sqlite3", ".db", ".pyc"}
PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\\\Users\\\\[A-Za-z0-9._-]+", re.I),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

errors: list[str] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel == "scripts/scan_public_tree.py":
        continue
    if path.suffix.lower() in PROHIBITED_SUFFIXES:
        errors.append(f"prohibited file: {rel}")
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"non-UTF8 file: {rel}")
        continue
    for pattern in PATH_PATTERNS:
        if pattern.search(text):
            errors.append(f"private path pattern: {rel}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"secret pattern: {rel}")

print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, indent=2))
raise SystemExit(1 if errors else 0)
