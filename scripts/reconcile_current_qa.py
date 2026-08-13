from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RESULTS_RELATIVE = "qa/CURRENT_TEST_RESULTS.json"
LOCK_RELATIVE = "qa/CURRENT_RELEASE_STATUS_LOCK.json"
RECONCILIATION_RELATIVE = "qa/CURRENT_QA_RECONCILIATION.json"
REPORT_RELATIVE = "qa/TEST_RESULTS.md"


def _count_passed(output: str) -> int:
    for line in output.splitlines():
        match = re.match(r"^\s*(\d+)\s+passed\b", line)
        if match:
            return int(match.group(1))
    return 0


def _head(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNSPECIFIED"


def reconcile(root: Path, *, target_head: str | None = None, public_scan_status: str | None = None) -> dict[str, Any]:
    results_path = root / RESULTS_RELATIVE
    lock_path = root / LOCK_RELATIVE
    raw_results = json.loads(results_path.read_text(encoding="utf-8")) if results_path.is_file() else None
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.is_file() else {}
    if isinstance(raw_results, dict):
        results = raw_results.get("targets")
    else:
        results = raw_results
    if not isinstance(results, list) or not isinstance(lock, dict):
        raise ValueError("current test results and release status lock must both be valid JSON with a target list")
    records: list[dict[str, Any]] = []
    for item in results:
        if not isinstance(item, dict):
            raise ValueError("current test results contains a non-object record")
        target = str(item.get("target", "")).strip()
        returncode = item.get("returncode")
        tested = bool(item.get("tested", True))
        if returncode is None and not tested:
            returncode = 0
        if not target or not isinstance(returncode, int):
            raise ValueError("each current test result requires target and integer returncode, or explicit tested=false")
        records.append({"target": target, "tests_passed": _count_passed(str(item.get("output", ""))), "returncode": returncode, "tested": tested})
    total = sum(record["tests_passed"] for record in records)
    failed = [record["target"] for record in records if record["returncode"] != 0]
    resolved_head = target_head or _head(root)
    lock["scope"] = "MAIN_MATURATION_PHASE1"
    lock["target_head"] = resolved_head
    lock["release"] = "MAIN_CANDIDATE_NOT_RELEASE"
    if public_scan_status is not None:
        lock["public_scan"] = public_scan_status
    lock["current_tests"] = f"{total} PASSED" if not failed else f"{total} PASSED / {len(failed)} FAILED_TARGETS"
    lock["current_targets"] = len(records)
    lock.setdefault("canonical_effect", "NONE")
    lock.setdefault("deployment", False)
    lock.setdefault("independent_ivv", "NOT_ACHIEVED")
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_lines = [
        "# Current Test Results",
        "",
        f"Target head: `{resolved_head}`. This report is generated from the current component runner output.",
        "",
        "| Target | Tests passed | Return code |",
        "|---|---:|---:|",
    ]
    report_lines.extend(f"| `{record['target']}` | {record['tests_passed']} | {record['returncode']} |" for record in records)
    report_lines.extend(["", f"**Total:** {total} passed across {len(records)} targets; failed targets: {len(failed)}.", ""])
    (root / REPORT_RELATIVE).write_text("\n".join(report_lines), encoding="utf-8")
    payload = {
        "schema_version": "0.1.0",
        "reconciliation_type": "CURRENT_TEST_EVIDENCE_TO_STATUS_LOCK",
        "target_head": resolved_head,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target_count": len(records),
        "test_count": total,
        "failed_targets": failed,
        "records": records,
        "status": "PASS" if not failed else "FAIL",
        "canonical_effect": "NONE",
        "deployment": False,
        "independent_ivv": "NOT_ACHIEVED",
        "mutation_scope": "QA_ARTIFACTS_ONLY",
    }
    (root / RECONCILIATION_RELATIVE).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reconcile current component test evidence into QA artifacts")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--target-head", default=None)
    parser.add_argument("--public-scan-status", choices=("PASS", "FAIL", "PENDING_FINAL_SCAN"), default=None)
    args = parser.parse_args(argv)
    payload = reconcile(args.root.resolve(), target_head=args.target_head, public_scan_status=args.public_scan_status)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
