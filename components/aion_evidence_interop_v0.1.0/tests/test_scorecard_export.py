from __future__ import annotations

import subprocess
from pathlib import Path

from aion_evidence_interop.scorecard_export import export_scorecard_crosswalk


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _by_name(report: dict[str, object]) -> dict[str, dict[str, object]]:
    return {
        item["check"]: item
        for item in report["checks"]  # type: ignore[index]
    }


def test_scorecard_crosswalk_is_explicitly_non_authoritative() -> None:
    report = export_scorecard_crosswalk(ROOT, _head())
    assert report["profile"] == "OPENSSF_SCORECARD_CROSSWALK_ONLY"
    assert report["openssf_scorecard_executed"] is False
    assert report["score"] is None
    assert report["boundaries"]["security_certification"] == "NOT_ESTABLISHED"  # type: ignore[index]
    assert report["boundaries"]["canonical_effect"] == "NONE"  # type: ignore[index]


def test_scorecard_crosswalk_separates_local_and_external_checks() -> None:
    report = export_scorecard_crosswalk(ROOT, _head())
    checks = _by_name(report)
    assert checks["Security-Policy"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["CI-Tests"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["SAST"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["Branch-Protection"]["status"] == "EXTERNAL_VERIFICATION_REQUIRED"
    assert checks["Code-Review"]["status"] == "EXTERNAL_VERIFICATION_REQUIRED"


def test_workflow_action_uses_are_sha_pinned_in_candidate_tree() -> None:
    report = export_scorecard_crosswalk(ROOT, _head())
    pinning = report["pinning_summary"]
    assert pinning["external_action_uses"] > 0  # type: ignore[index]
    assert pinning["mutable_external_action_uses"] == []  # type: ignore[index]
