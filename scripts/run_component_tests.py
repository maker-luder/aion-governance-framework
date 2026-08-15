from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


def _sanitize(text: str) -> str:
    return text.replace(str(ROOT), "<CANDIDATE_ROOT>")


def _test_count(output: str) -> int:
    matches = re.findall(r"(\d+) passed", output)
    return int(matches[-1]) if matches else 0


results: list[dict[str, object]] = []
for target in ELIGIBLE_TARGETS:
    relative = str(target.relative_to(ROOT))
    tests_dir = target / "tests"
    if not tests_dir.is_dir():
        results.append(
            {
                "target": relative,
                "status": "NO_TEST_DIRECTORY",
                "tested": False,
                "returncode": None,
                "passed": 0,
                "failed": 0,
                "coverage": "NOT_APPLICABLE_RESEARCH_ONLY_SURFACE",
                "output": "No tests directory is present; retained as an explicit research-only non-applicability disposition.",
            }
        )
        print(f"[{target.name}] status=NO_TEST_DIRECTORY (explicit non-applicability)")
        continue
    ordered = [target / "src", ROOT] + [path for path in SOURCE_ROOTS if path != target / "src" and path.is_dir()]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in ordered)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-o", "addopts="],
        cwd=target,
        text=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = _sanitize(proc.stdout)
    failed_match = re.search(r"(\d+) failed", output)
    failed = int(failed_match.group(1)) if failed_match else 0
    passed = _test_count(output)
    results.append(
        {
            "target": relative,
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "tested": True,
            "returncode": proc.returncode,
            "passed": passed,
            "failed": failed,
            "coverage": "PENDING_BRANCH_COVERAGE_RUN",
            "output": output,
        }
    )
    print(f"[{target.name}] returncode={proc.returncode} passed={passed} failed={failed}")
    print(proc.stdout)

summary = {
    "eligible_target_count": len(ELIGIBLE_TARGETS),
    "tested_target_count": sum(bool(item["tested"]) for item in results),
    "non_applicable_target_count": sum(not bool(item["tested"]) for item in results),
    "failed_target_count": sum(item["status"] == "FAIL" for item in results),
    "total_passed": sum(int(item["passed"]) for item in results),
    "total_failed": sum(int(item["failed"]) for item in results),
}
output_path = ROOT / "qa" / "CURRENT_TEST_RESULTS.json"
output_path.write_text(json.dumps({"schema_version": "2.0", "scope": "FINAL_FORMAL_RESEARCH_TREE", "target_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "summary": summary, "targets": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
raise SystemExit(0 if summary["failed_target_count"] == 0 else 1)
