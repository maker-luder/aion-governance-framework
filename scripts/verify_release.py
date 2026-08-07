from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "FILE_MANIFEST.json"
SUMS = ROOT / "manifest" / "SHA256SUMS.txt"

PROHIBITED_SUFFIXES = {".zip", ".whl", ".sqlite3", ".db", ".pyc"}
PATH_PATTERNS = [re.compile(r"[A-Za-z]:\\\\Users\\\\[A-Za-z0-9._-]+", re.I), re.compile(r"/home/[A-Za-z0-9._-]+/"), re.compile("hs" + "upo", re.I)]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

errors: list[str] = []
records = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
for record in records:
    path = ROOT / record["path"]
    if not path.is_file():
        errors.append(f"missing: {record['path']}")
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != record["sha256"]:
        errors.append(f"hash mismatch: {record['path']}")

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel == "scripts/verify_release.py":
        continue
    if path.suffix.lower() in PROHIBITED_SUFFIXES:
        errors.append(f"prohibited file: {rel}")
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

expected = {line.split("  ", 1)[1]: line.split("  ", 1)[0] for line in SUMS.read_text(encoding="utf-8").splitlines() if "  " in line}
if len(expected) != len(records):
    errors.append("SHA256SUMS count differs from manifest")

print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, "files": len(records)}, indent=2))
raise SystemExit(1 if errors else 0)
