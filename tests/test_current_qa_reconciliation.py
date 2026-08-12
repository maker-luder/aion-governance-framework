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
    lock = json.loads((root / "qa/CURRENT_RELEASE_STATUS_LOCK.json").read_text(encoding="utf-8"))
    assert lock["current_tests"] == "3 PASSED"
    assert lock["current_targets"] == 2
    assert "Target head: `abc123`" in (root / "qa/TEST_RESULTS.md").read_text(encoding="utf-8")
    assert json.loads((root / "qa/CURRENT_QA_RECONCILIATION.json").read_text(encoding="utf-8"))["canonical_effect"] == "NONE"


def test_reconcile_returns_fail_for_failed_target(tmp_path: Path) -> None:
    payload = reconciler.reconcile(make_root(tmp_path, failed=True), target_head="abc123")
    assert payload["status"] == "FAIL"
    assert payload["failed_targets"] == ["research-labs/b"]
