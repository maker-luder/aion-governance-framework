from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_current_license_status_is_reconciled_without_erasing_history() -> None:
    release_status = _read("docs/RELEASE_STATUS.md")
    roadmap = _read("docs/ROADMAP_AFTER_PUBLIC_RC.md")
    qa_summary = _read("qa/QA_SUMMARY.md")
    checklist = _read("qa/PUBLIC_RELEASE_CHECKLIST.md")
    status_lock = json.loads(_read("qa/CURRENT_RELEASE_STATUS_LOCK.json"))
    release_evidence = json.loads(_read("qa/RELEASE_EVIDENCE.json"))

    assert "LICENSE_SELECTION = APACHE_2_0_SELECTED" in release_status
    assert "LICENSE_SELECTION = PENDING_OWNER_DECISION" not in release_status
    assert "OWNER_SELECTION_REQUIRED" in release_status.split("## Current GitHub reconstruction", 1)[0]
    assert "| License selection | RESOLVED_APACHE_2_0 |" in roadmap
    assert status_lock["license_status"] == "APACHE_2_0_SELECTED"
    assert release_evidence["license_status"] == "APACHE_2_0_SELECTED"
    assert "- [x] Final public license selected by Owner for project-owned repository material;" in checklist
    assert "final public license selection remains subject to the Owner gate" not in qa_summary
    assert "third-party compatibility remains separately review-gated" in qa_summary
