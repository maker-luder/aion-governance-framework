from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "old_412_test_claim": re.compile(r"412\s+PASSED"),
    "old_whole_system_not_executed": re.compile(r"whole_system_validation\s*[=:]\s*[\"'`]?NOT[_ ]EXECUTED", re.IGNORECASE),
    "old_25_target_claim": re.compile(r"(?:\b25\s+targets\b|\"target_count\"\s*:\s*25)", re.IGNORECASE),
}
EXCLUDED = {
    Path("docs/REPAIR_V2_SOURCE_RECONCILIATION.md"),
    Path("docs/REPAIR_V2_REPLAY_LEDGER.md"),
}
errors: list[str] = []
scanned = 0
for top in (ROOT / "docs", ROOT / "qa"):
    for path in sorted(top.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if "historical" in relative.parts or relative in EXCLUDED:
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{name}: {relative}")
result = {"status": "PASS" if not errors else "FAIL", "scanned_files": scanned, "errors": errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
