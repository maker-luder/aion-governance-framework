from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import reconcile_current_qa as reconciler  # noqa: E402


def make_root(tmp_path: Path, *, failed: bool = False) -> Path:
    root = tmp_path / "repo"
    (root / "qa").mkdir(parents=True)
    (root / "qa" / "CURRENT_TEST_RESULTS.json").write_text(
        json.dumps(
            [
                {"target": "components/a", "returncode": 0, "output": "2 passed in 0.01s\n"},
                {"target": "research-labs/b", "returncode": 1 if failed else 0, "output": "1 passed in 0.01s\n"},
            ]
        ),
        encoding="utf-8",
    )
    (root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").write_text(
        json.dumps(
            {
                "current_tests": "stale",
                "current_targets": 99,
                "eligible_target_count": 50,
                "tested_target_count": 47,
                "non_applicable_target_count": 3,
                "whole_system_validation": "NOT_EXECUTED",
                "public_scan": "PASS",
                "canonical_effect": "NONE",
                "deployment": False,
                "independent_ivv": "NOT_ACHIEVED",
            }
        ),
        encoding="utf-8",
    )
    return root


def make_schema_v2_root(tmp_path: Path, *, stale_summary: bool = False) -> Path:
    root = tmp_path / "repo-v2"
    (root / "qa").mkdir(parents=True)
    results = {
        "schema_version": "2.0",
        "scope": "FINAL_FORMAL_RESEARCH_TREE",
        "summary": {
            "eligible_target_count": 99 if stale_summary else 2,
            "tested_target_count": 1,
            "non_applicable_target_count": 1,
            "failed_target_count": 0,
            "total_passed": 2,
        },
        "targets": [
            {"target": "components/a", "tested": True, "returncode": 0, "output": "2 passed in 0.01s\n"},
            {"target": "research-labs/design-only", "tested": False, "returncode": None, "output": ""},
        ],
    }
    (root / "qa" / "CURRENT_TEST_RESULTS.json").write_text(json.dumps(results), encoding="utf-8")
    (root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").write_text(
        json.dumps(
            {
                "current_tests": "1503 PASSED",
                "current_targets": 82,
                "eligible_target_count": 50,
                "tested_target_count": 47,
                "non_applicable_target_count": 3,
                "whole_system_validation": "21 TEST_CASES / 11 SCENARIO_CLASSES / PASS",
                "public_scan": "PASS",
                "canonical_effect": "NONE",
                "deployment": False,
                "independent_ivv": "NOT_ACHIEVED",
            }
        ),
        encoding="utf-8",
    )
    return root


def test_reconcile_updates_lock_and_reports(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    payload = reconciler.reconcile(root, target_head="abc123")
    assert payload["status"] == "PASS"
    assert payload["test_count"] == 3
    assert payload["target_count"] == 2
    assert payload["eligible_target_count"] == 2
    assert payload["tested_target_count"] == 2
    assert payload["non_applicable_target_count"] == 0
    assert payload["whole_system_validation"] == "NOT_ESTABLISHED"

    lock = json.loads((root / "qa/CURRENT_RELEASE_STATUS_LOCK.json").read_text(encoding="utf-8"))
    assert lock["current_tests"] == "3 PASSED"
    assert lock["current_targets"] == 2
    assert lock["eligible_target_count"] == 2
    assert lock["tested_target_count"] == 2
    assert lock["non_applicable_target_count"] == 0
    assert lock["whole_system_test_suite_status"] == "NOT_EXECUTED"
    assert lock["whole_system_validation"] == "NOT_ESTABLISHED"
    assert "Target head: `abc123`" in (root / "qa/TEST_RESULTS.md").read_text(encoding="utf-8")
    assert json.loads((root / "qa/CURRENT_QA_RECONCILIATION.json").read_text(encoding="utf-8"))["canonical_effect"] == "NONE"


def test_reconcile_schema_v2_overwrites_stale_lock_counts_from_bound_results(tmp_path: Path) -> None:
    root = make_schema_v2_root(tmp_path)
    payload = reconciler.reconcile(root, target_head="abc123")
    assert payload["eligible_target_count"] == 2
    assert payload["tested_target_count"] == 1
    assert payload["non_applicable_target_count"] == 1
    assert payload["test_count"] == 2

    lock = json.loads((root / "qa/CURRENT_RELEASE_STATUS_LOCK.json").read_text(encoding="utf-8"))
    assert lock["current_targets"] == 2
    assert lock["eligible_target_count"] == 2
    assert lock["tested_target_count"] == 1
    assert lock["non_applicable_target_count"] == 1
    assert lock["whole_system_test_suite_status"] == "21 TEST_CASES / 11 SCENARIO_CLASSES / PASS"
    assert lock["whole_system_validation"] == "NOT_ESTABLISHED"


def test_reconcile_rejects_internally_stale_schema_v2_summary(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="summary is stale/inconsistent"):
        reconciler.reconcile(make_schema_v2_root(tmp_path, stale_summary=True), target_head="abc123")


def test_reconcile_returns_fail_for_failed_target(tmp_path: Path) -> None:
    payload = reconciler.reconcile(make_root(tmp_path, failed=True), target_head="abc123")
    assert payload["status"] == "FAIL"
    assert payload["failed_targets"] == ["research-labs/b"]
