from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "manifest"
MANIFEST_DIR.mkdir(exist_ok=True)
excluded = {"manifest/FILE_MANIFEST.json", "manifest/SHA256SUMS.txt"}
files = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or ".git" in path.parts:
        continue
    if any(part in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"} for part in path.parts):
        continue
    if path.name == ".coverage" or path.suffix == ".pyc":
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel in excluded:
        continue
    data = path.read_bytes()
    files.append({"path": rel, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
(MANIFEST_DIR / "FILE_MANIFEST.json").write_text(json.dumps({"schema_version": "1.0", "files": files}, indent=2) + "\n", encoding="utf-8")
(MANIFEST_DIR / "SHA256SUMS.txt").write_text("".join(f"{item['sha256']}  {item['path']}\n" for item in files), encoding="utf-8")
print(f"wrote {len(files)} records")
