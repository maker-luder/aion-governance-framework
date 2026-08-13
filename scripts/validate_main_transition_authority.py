from __future__ import annotations

import argparse
import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BEGIN = "<!-- MAIN_TRANSITION_AUTHORITY_RECEIPT_BEGIN -->"
END = "<!-- MAIN_TRANSITION_AUTHORITY_RECEIPT_END -->"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
STATEMENT = (
    "I explicitly approve merging the specified target PR at the specified exact "
    "head into main for this action."
)


@dataclass(frozen=True, slots=True)
class AccountEvidence:
    github_event_sender_match: bool
    pr_body_edit_event: bool
    target_pr_match: bool | None = None
    target_head_match: bool | None = None
    timestamp_fresh: bool | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "evidence_scope": "AUTHENTICATED_GITHUB_ACCOUNT_EVENT_ONLY",
            "github_event_sender_match": self.github_event_sender_match,
            "pr_body_edit_event": self.pr_body_edit_event,
            "target_pr_match": self.target_pr_match,
            "target_head_match": self.target_head_match,
            "timestamp_fresh": self.timestamp_fresh,
        }


@dataclass(frozen=True, slots=True)
class GateResult:
    status: str
    diagnostics: tuple[str, ...]
    account_evidence: AccountEvidence
    target_pr: int | None = None
    target_head: str | None = None
    human_owner_explicit_approval: str = "NOT_ESTABLISHED"
    human_owner_intent_source: str = "NOT_ESTABLISHED"
    mutation_performed: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False
    fail_closed_to: str = "HOLD"

    def as_dict(self) -> dict[str, Any]:
        return {
            "gate": "MAIN_TRANSITION_AUTHORITY",
            "status": self.status,
            "diagnostics": list(self.diagnostics),
            "target_pr": self.target_pr,
            "target_head": self.target_head,
            "repository_account_evidence": self.account_evidence.as_dict(),
            "human_authority_assertion": {
                "human_owner_explicit_approval": self.human_owner_explicit_approval,
                "human_owner_intent_source": self.human_owner_intent_source,
            },
            "validator_epistemic_boundary": {
                "human_identity_independently_verified": False,
                "human_presence_independently_verified": False,
                "human_intent_independently_verified": False,
                "human_presence_attestation": "EXTERNAL_TO_VALIDATOR",
                "structural_receipt_pass_is_independent_human_identity_proof": False,
            },
            "mutation_performed": self.mutation_performed,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "fail_closed_to": self.fail_closed_to,
        }


def _parse_time(value: Any, label: str, diagnostics: list[str]) -> datetime | None:
    if not isinstance(value, str):
        diagnostics.append(f"{label} is missing or not a string")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        diagnostics.append(f"{label} is not RFC3339-compatible")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        diagnostics.append(f"{label} must include an explicit timezone")
        return None
    return parsed.astimezone(timezone.utc)


def _extract_receipt(body: Any) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(body, str):
        return None, "pull request body is missing"
    if body.count(BEGIN) != 1 or body.count(END) != 1:
        return None, "exactly one authority receipt marker block is required"
    payload = body.split(BEGIN, 1)[1].split(END, 1)[0].strip()
    if payload.startswith("```json") and payload.endswith("```"):
        payload = payload[len("```json") : -len("```")].strip()
    try:
        record = json.loads(payload)
    except json.JSONDecodeError as exc:
        return None, f"authority receipt JSON is invalid: {exc}"
    if not isinstance(record, dict):
        return None, "authority receipt must be a JSON object"
    return record, None


def validate_record(
    record: dict[str, Any] | None,
    *,
    expected_repository: str,
    expected_pr: int,
    expected_head: str,
    expected_ref: str,
    approval_event_time: datetime,
    event_action: str,
    body_was_edited: bool,
    event_sender: str,
    human_owner_login: str,
    freshness_seconds: int = 300,
) -> GateResult:
    diagnostics: list[str] = []
    sender_match = event_sender == human_owner_login
    body_edit_event = event_action == "edited" and body_was_edited
    base_evidence = AccountEvidence(sender_match, body_edit_event)
    if record is None:
        return GateResult(
            "HOLD", ("authority receipt is missing",), base_evidence, expected_pr, expected_head
        )

    required_constants = {
        "schema_version": "0.1.0",
        "record_type": "MAIN_TRANSITION_AUTHORITY_RECEIPT",
        "repository": expected_repository,
        "action": "MERGE_PR_INTO_MAIN",
        "target_branch": "main",
        "target_pr": expected_pr,
        "target_head": expected_head,
        "human_owner_explicit_approval": "GIVEN",
        "explicit_statement": STATEMENT,
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
    expected_keys = set(required_constants) | {
        "approval_id",
        "approval_time",
        "approval_source",
    }
    unexpected_keys = sorted(set(record) - expected_keys)
    missing_keys = sorted(expected_keys - set(record))
    if unexpected_keys:
        diagnostics.append(f"unexpected receipt fields: {unexpected_keys}")
    if missing_keys:
        diagnostics.append(f"missing receipt fields: {missing_keys}")
    for key, expected in required_constants.items():
        if record.get(key) != expected:
            diagnostics.append(f"{key} must equal {expected!r}")

    try:
        uuid.UUID(str(record.get("approval_id")))
    except (ValueError, AttributeError):
        diagnostics.append("approval_id must be a UUID")

    target_pr_match = record.get("target_pr") == expected_pr
    target_head_match = record.get("target_head") == expected_head
    if not SHA40.fullmatch(str(record.get("target_head", ""))):
        diagnostics.append("target_head must be an exact lowercase 40-hex commit SHA")

    source = record.get("approval_source")
    if not isinstance(source, dict):
        diagnostics.append("approval_source must be an object")
    else:
        if set(source) != {"kind", "ref", "recorded_by"}:
            diagnostics.append("approval_source fields must be exactly kind, ref, and recorded_by")
        if source.get("kind") != "GITHUB_PR_BODY_EDIT":
            diagnostics.append("approval_source.kind must be GITHUB_PR_BODY_EDIT")
        if source.get("ref") != expected_ref:
            diagnostics.append("approval_source.ref must match the target pull request")
        if source.get("recorded_by") != "HUMAN_OWNER":
            diagnostics.append("approval_source.recorded_by must be HUMAN_OWNER")

    if event_action != "edited":
        diagnostics.append("fresh approval must arrive in a pull_request edited event")
    if not body_was_edited:
        diagnostics.append("fresh approval event must specifically edit the pull request body")
    if not sender_match:
        diagnostics.append("receipt edit sender does not match configured Human Owner login")

    approval_time = _parse_time(record.get("approval_time"), "approval_time", diagnostics)
    timestamp_fresh = False
    if approval_time is not None:
        delta = abs((approval_event_time - approval_time).total_seconds())
        timestamp_fresh = delta <= freshness_seconds
        if not timestamp_fresh:
            diagnostics.append(
                f"approval_time is not fresh for the receipt edit event ({delta:.0f}s delta)"
            )

    account_evidence = AccountEvidence(
        sender_match,
        body_edit_event,
        target_pr_match,
        target_head_match,
        timestamp_fresh,
    )
    return GateResult(
        "PASS" if not diagnostics else "HOLD",
        tuple(diagnostics),
        account_evidence,
        expected_pr,
        expected_head,
        str(record.get("human_owner_explicit_approval", "NOT_ESTABLISHED")),
        str(record.get("human_owner_intent_source", "NOT_ESTABLISHED")),
    )


def validate_event(
    event: dict[str, Any],
    *,
    expected_repository: str,
    human_owner_login: str,
) -> GateResult:
    action = str(event.get("action", ""))
    changes = event.get("changes") if isinstance(event.get("changes"), dict) else {}
    body_was_edited = isinstance(changes.get("body"), dict)
    sender = event.get("sender") if isinstance(event.get("sender"), dict) else {}
    sender_login = str(sender.get("login", ""))
    base_evidence = AccountEvidence(
        sender_login == human_owner_login,
        action == "edited" and body_was_edited,
    )
    pull = event.get("pull_request")
    if not isinstance(pull, dict):
        return GateResult("HOLD", ("event does not contain a pull_request object",), base_evidence)
    base = pull.get("base") if isinstance(pull.get("base"), dict) else {}
    head = pull.get("head") if isinstance(pull.get("head"), dict) else {}
    expected_pr = event.get("number")
    expected_head = head.get("sha")
    expected_ref = pull.get("html_url")
    if base.get("ref") != "main":
        return GateResult("HOLD", ("target branch is not main",), base_evidence)
    if not isinstance(expected_pr, int) or not isinstance(expected_head, str) or not isinstance(expected_ref, str):
        return GateResult(
            "HOLD",
            ("event target PR, exact head, or PR URL is missing",),
            base_evidence,
        )
    event_time_diagnostics: list[str] = []
    event_time = _parse_time(
        pull.get("updated_at"), "pull_request.updated_at", event_time_diagnostics
    )
    if event_time is None:
        return GateResult(
            "HOLD", tuple(event_time_diagnostics), base_evidence, expected_pr, expected_head
        )
    record, extract_error = _extract_receipt(pull.get("body"))
    if extract_error:
        return GateResult(
            "HOLD", (extract_error,), base_evidence, expected_pr, expected_head
        )
    return validate_record(
        record,
        expected_repository=expected_repository,
        expected_pr=expected_pr,
        expected_head=expected_head,
        expected_ref=expected_ref,
        approval_event_time=event_time,
        event_action=action,
        body_was_edited=body_was_edited,
        event_sender=sender_login,
        human_owner_login=human_owner_login,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed structural main-transition authority receipt gate"
    )
    parser.add_argument("--github-event", type=Path, required=True)
    parser.add_argument("--expected-repository", required=True)
    parser.add_argument("--human-owner-login", required=True)
    args = parser.parse_args(argv)
    empty_evidence = AccountEvidence(False, False)
    try:
        event = json.loads(args.github_event.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result = GateResult(
            "HOLD", (f"event file is missing: {args.github_event}",), empty_evidence
        )
    except json.JSONDecodeError as exc:
        result = GateResult("HOLD", (f"event JSON is invalid: {exc}",), empty_evidence)
    else:
        result = validate_event(
            event,
            expected_repository=args.expected_repository,
            human_owner_login=args.human_owner_login,
        )
    print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    return 0 if result.status == "PASS" else 10


if __name__ == "__main__":
    raise SystemExit(main())
