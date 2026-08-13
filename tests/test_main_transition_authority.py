from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_main_transition_authority as gate  # noqa: E402

HEAD = "a" * 40
PR_URL = "https://github.com/maker-luder/aion-governance-framework/pull/99"
EVENT_TIME = "2026-08-13T12:00:00Z"


def valid_receipt() -> dict[str, object]:
    return {
        "schema_version": "0.1.0",
        "record_type": "MAIN_TRANSITION_AUTHORITY_RECEIPT",
        "approval_id": "12345678-1234-4234-8234-123456789abc",
        "repository": "maker-luder/aion-governance-framework",
        "action": "MERGE_PR_INTO_MAIN",
        "target_branch": "main",
        "target_pr": 99,
        "target_head": HEAD,
        "approval_time": EVENT_TIME,
        "human_owner_explicit_approval": "GIVEN",
        "explicit_statement": gate.STATEMENT,
        "approval_source": {
            "kind": "GITHUB_PR_BODY_EDIT",
            "ref": PR_URL,
            "recorded_by": "HUMAN_OWNER",
        },
        "fresh_for_current_action": True,
        "action_specific": True,
        "target_specific": True,
        "prior_authorization_inherited": False,
        "candidate_scope_approval_used_as_merge_authority": False,
        "autonomous_research_permission_used_as_merge_authority": False,
        "qa_pass_used_as_merge_authority": False,
        "ai_review_used_as_human_owner_merge_approval": False,
        "contradictions": [],
        "decision": "APPROVED",
        "fail_closed_to": "HOLD",
        "canonical_effect": "NONE",
        "deployment": False,
    }


def event_for(record: dict[str, object] | None, *, action: str = "edited", sender: str = "maker-luder") -> dict[str, object]:
    if record is None:
        body = "candidate only"
    else:
        body = f"{gate.BEGIN}\n```json\n{json.dumps(record)}\n```\n{gate.END}"
    return {
        "action": action,
        "number": 99,
        "changes": {"body": {"from": "candidate only"}},
        "sender": {"login": sender},
        "pull_request": {
            "html_url": PR_URL,
            "updated_at": EVENT_TIME,
            "body": body,
            "base": {"ref": "main"},
            "head": {"sha": HEAD},
        },
    }


def validate(event: dict[str, object]) -> gate.GateResult:
    return gate.validate_event(
        event,
        expected_repository="maker-luder/aion-governance-framework",
        human_owner_login="maker-luder",
    )


def test_exact_fresh_action_specific_receipt_passes_without_mutation() -> None:
    event = event_for(valid_receipt())
    before = copy.deepcopy(event)
    result = validate(event)
    assert result.status == "PASS"
    assert result.mutation_performed is False
    assert result.canonical_effect == "NONE"
    assert result.deployment is False
    assert event == before


def test_missing_receipt_fails_closed_to_hold() -> None:
    result = validate(event_for(None))
    assert result.status == "HOLD"
    assert result.fail_closed_to == "HOLD"


def test_exact_head_mismatch_fails_closed() -> None:
    record = valid_receipt()
    record["target_head"] = "b" * 40
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert any("target_head" in item for item in result.diagnostics)


def test_qa_pass_cannot_be_used_as_merge_authority() -> None:
    record = valid_receipt()
    record["qa_pass_used_as_merge_authority"] = True
    result = validate(event_for(record))
    assert result.status == "HOLD"


def test_prior_authorization_cannot_be_inherited() -> None:
    record = valid_receipt()
    record["prior_authorization_inherited"] = True
    result = validate(event_for(record))
    assert result.status == "HOLD"


def test_contradiction_fails_closed() -> None:
    record = valid_receipt()
    record["contradictions"] = ["MERGE_MAIN = NOT_APPROVED"]
    result = validate(event_for(record))
    assert result.status == "HOLD"


def test_non_edit_event_is_not_fresh_approval() -> None:
    result = validate(event_for(valid_receipt(), action="synchronize"))
    assert result.status == "HOLD"
    assert any("edited event" in item for item in result.diagnostics)


def test_title_only_edit_is_not_fresh_body_approval() -> None:
    event = event_for(valid_receipt())
    event["changes"] = {"title": {"from": "old title"}}
    result = validate(event)
    assert result.status == "HOLD"
    assert any("specifically edit" in item for item in result.diagnostics)


def test_sender_must_match_configured_human_owner_login() -> None:
    result = validate(event_for(valid_receipt(), sender="automation-account"))
    assert result.status == "HOLD"


def test_stale_approval_time_fails_closed() -> None:
    record = valid_receipt()
    record["approval_time"] = "2026-08-13T11:00:00Z"
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert any("not fresh" in item for item in result.diagnostics)


def test_approval_time_requires_timezone() -> None:
    record = valid_receipt()
    record["approval_time"] = "2026-08-13T12:00:00"
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert any("timezone" in item for item in result.diagnostics)


def test_unknown_receipt_field_fails_closed() -> None:
    record = valid_receipt()
    record["qa_pass_implies_merge"] = True
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert any("unexpected receipt fields" in item for item in result.diagnostics)
