from __future__ import annotations

import copy
import json
import sys
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
        "account_authentication_evidence": "GITHUB_EVENT_SENDER_MATCH_ONLY",
        "human_owner_intent_source": "EXTERNAL_ATTESTATION",
        "human_identity_independently_verified": False,
        "human_presence_independently_verified": False,
        "human_intent_independently_verified": False,
        "human_presence_attestation": "EXTERNAL_TO_VALIDATOR",
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


def marked_body(record: dict[str, object]) -> str:
    return f"{gate.BEGIN}\n```json\n{json.dumps(record)}\n```\n{gate.END}"


def event_for(
    record: dict[str, object] | None,
    *,
    action: str = "edited",
    sender: str = "maker-luder",
) -> dict[str, object]:
    return {
        "action": action,
        "number": 99,
        "changes": {"body": {"from": "candidate only"}},
        "sender": {"login": sender},
        "pull_request": {
            "html_url": PR_URL,
            "updated_at": EVENT_TIME,
            "body": "candidate only" if record is None else marked_body(record),
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


def test_structural_pass_preserves_external_human_identity_boundary_without_mutation() -> None:
    event = event_for(valid_receipt())
    before = copy.deepcopy(event)
    result = validate(event)
    payload = result.as_dict()
    assert result.status == "PASS"
    assert result.mutation_performed is False
    assert payload["repository_account_evidence"] == {
        "evidence_scope": "AUTHENTICATED_GITHUB_ACCOUNT_EVENT_ONLY",
        "github_event_sender_match": True,
        "pr_body_edit_event": True,
        "target_pr_match": True,
        "target_head_match": True,
        "timestamp_fresh": True,
    }
    assert payload["human_authority_assertion"] == {
        "human_owner_explicit_approval": "GIVEN",
        "human_owner_intent_source": "EXTERNAL_ATTESTATION",
    }
    boundary = payload["validator_epistemic_boundary"]
    assert boundary["human_identity_independently_verified"] is False
    assert boundary["human_presence_independently_verified"] is False
    assert boundary["human_intent_independently_verified"] is False
    assert boundary["human_presence_attestation"] == "EXTERNAL_TO_VALIDATOR"
    assert boundary["structural_receipt_pass_is_independent_human_identity_proof"] is False
    assert result.canonical_effect == "NONE"
    assert result.deployment is False
    assert event == before


def test_valid_fixture_conforms_to_schema() -> None:
    from jsonschema import Draft202012Validator, FormatChecker

    schema = json.loads(
        (ROOT / "schemas" / "main_transition_authority_receipt_v0.1.0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert list(validator.iter_errors(valid_receipt())) == []


def test_missing_receipt_fails_closed_to_hold() -> None:
    result = validate(event_for(None))
    assert result.status == "HOLD"
    assert result.fail_closed_to == "HOLD"


def test_different_sender_fails_closed() -> None:
    result = validate(event_for(valid_receipt(), sender="automation-account"))
    assert result.status == "HOLD"
    assert result.account_evidence.github_event_sender_match is False


def test_exact_head_mismatch_fails_closed() -> None:
    record = valid_receipt()
    record["target_head"] = "b" * 40
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert result.account_evidence.target_head_match is False


def test_prior_authorization_cannot_be_inherited() -> None:
    record = valid_receipt()
    record["prior_authorization_inherited"] = True
    assert validate(event_for(record)).status == "HOLD"


def test_qa_pass_cannot_be_used_as_merge_authority() -> None:
    record = valid_receipt()
    record["qa_pass_used_as_merge_authority"] = True
    assert validate(event_for(record)).status == "HOLD"


def test_ai_review_cannot_be_used_as_owner_approval() -> None:
    record = valid_receipt()
    record["ai_review_used_as_human_owner_merge_approval"] = True
    assert validate(event_for(record)).status == "HOLD"


def test_autonomous_research_permission_cannot_be_used_as_merge_authority() -> None:
    record = valid_receipt()
    record["autonomous_research_permission_used_as_merge_authority"] = True
    assert validate(event_for(record)).status == "HOLD"


def test_stale_approval_time_fails_closed() -> None:
    record = valid_receipt()
    record["approval_time"] = "2026-08-13T11:00:00Z"
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert result.account_evidence.timestamp_fresh is False


def test_non_body_edit_event_fails_closed() -> None:
    event = event_for(valid_receipt())
    event["changes"] = {"title": {"from": "old title"}}
    result = validate(event)
    assert result.status == "HOLD"
    assert result.account_evidence.pr_body_edit_event is False


def test_contradiction_fails_closed() -> None:
    record = valid_receipt()
    record["contradictions"] = ["MERGE_MAIN = NOT_APPROVED"]
    assert validate(event_for(record)).status == "HOLD"


def test_malformed_receipt_fails_closed() -> None:
    event = event_for(valid_receipt())
    event["pull_request"]["body"] = f"{gate.BEGIN}\n{{bad json\n{gate.END}"
    result = validate(event)
    assert result.status == "HOLD"
    assert any("JSON is invalid" in item for item in result.diagnostics)


def test_duplicate_receipt_fails_closed() -> None:
    event = event_for(valid_receipt())
    body = event["pull_request"]["body"]
    event["pull_request"]["body"] = f"{body}\n{body}"
    result = validate(event)
    assert result.status == "HOLD"
    assert any("exactly one" in item for item in result.diagnostics)


def test_unknown_receipt_field_fails_closed() -> None:
    record = valid_receipt()
    record["qa_pass_implies_merge"] = True
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert any("unexpected receipt fields" in item for item in result.diagnostics)


def test_human_presence_claim_cannot_be_elevated() -> None:
    record = valid_receipt()
    record["human_presence_independently_verified"] = True
    result = validate(event_for(record))
    assert result.status == "HOLD"
    assert any("human_presence_independently_verified" in item for item in result.diagnostics)
