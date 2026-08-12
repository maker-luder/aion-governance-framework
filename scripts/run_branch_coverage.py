from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVERAGE_DIR = ROOT / "qa" / "coverage"
COVERAGE_DIR.mkdir(parents=True, exist_ok=True)
ELIGIBLE_TARGETS = sorted(
    [path for top in ("components", "examples", "research-labs") for path in (ROOT / top).iterdir() if path.is_dir()]
)
SOURCE_ROOTS = list(
    dict.fromkeys(
        sorted(ROOT.glob("components/*/src"))
        + sorted(ROOT.glob("examples/*/src"))
        + sorted(ROOT.glob("research-labs/*/src"))
    )
)


def safe_name(relative: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", relative)


def sanitize(text: str) -> str:
    return text.replace(str(ROOT), "<CANDIDATE_ROOT>")


results: list[dict[str, object]] = []
for target in ELIGIBLE_TARGETS:
    relative = str(target.relative_to(ROOT))
    if not (target / "tests").is_dir():
        results.append(
            {
                "target": relative,
                "status": "NOT_APPLICABLE",
                "tested": False,
                "coverage_percent": None,
                "branch_coverage": True,
                "reason": "No tests directory; research-only surface retained with explicit non-applicability.",
            }
        )
        continue
    ordered = [target / "src"] + [path for path in SOURCE_ROOTS if path != target / "src" and path.is_dir()]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in ordered)
    raw_path = COVERAGE_DIR / f"{safe_name(relative)}.json"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-o",
            "addopts=",
            "--cov=src",
            "--cov-branch",
            f"--cov-report=json:{raw_path}",
        ],
        cwd=target,
        text=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    percent: float | None = None
    if raw_path.exists():
        try:
            percent = float(json.loads(raw_path.read_text(encoding="utf-8"))["totals"]["percent_covered"])
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            percent = None
    results.append(
        {
            "target": relative,
            "status": "MEASURED" if proc.returncode == 0 and percent is not None else "FAILED",
            "tested": True,
            "returncode": proc.returncode,
            "coverage_percent": percent,
            "branch_coverage": True,
            "raw_evidence": str(raw_path.relative_to(ROOT)),
            "output": sanitize(proc.stdout),
        }
    )
    print(f"[{relative}] returncode={proc.returncode} coverage={percent}")

summary = {
    "eligible_target_count": len(ELIGIBLE_TARGETS),
    "measured_target_count": sum(bool(item["tested"]) for item in results),
    "not_applicable_target_count": sum(not bool(item["tested"]) for item in results),
    "failed_target_count": sum(item["status"] == "FAILED" for item in results),
    "branch_coverage": True,
    "threshold_policy": "REPORT_ONLY_NO_UNJUSTIFIED_GLOBAL_THRESHOLD",
}
payload = {
    "schema_version": "2.0",
    "generated_at": datetime.now(UTC).isoformat(),
    "scope": "REVIEW_CANDIDATE_V2",
    "summary": summary,
    "targets": results,
}
(ROOT / "qa" / "CURRENT_COVERAGE_RESULTS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raise SystemExit(0 if summary["failed_target_count"] == 0 else 1)
