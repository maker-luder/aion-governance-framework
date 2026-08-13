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
class GateResult:
    status: str
    diagnostics: tuple[str, ...]
    target_pr: int | None = None
    target_head: str | None = None
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
            "mutation_performed": self.mutation_performed,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "fail_closed_to": self.fail_closed_to,
            "human_identity_attestation": "EXTERNAL_TO_THIS_VALIDATOR",
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
    if record is None:
        return GateResult("HOLD", ("authority receipt is missing",), expected_pr, expected_head)

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
        "fresh_for_current_action": True,
        "action_specific": True,
        "target_specific": True,
        "prior_authorization_inherited": False,
        "candidate_scope_approval_used_as_merge_authority": False,
        "autonomous_research_permission_used_as_merge_authority": False,
        "qa_pass_used_as_merge_authority": False,
        "ai_review_used_as_human_owner_merge_approval": False,
        "decision": "APPROVED",
        "fail_closed_to": "HOLD",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    expected_keys = set(required_constants) | {
        "approval_id",
        "approval_time",
        "approval_source",
        "contradictions",
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

    approval_id = record.get("approval_id")
    try:
        uuid.UUID(str(approval_id))
    except (ValueError, AttributeError):
        diagnostics.append("approval_id must be a UUID")

    if not SHA40.fullmatch(str(record.get("target_head", ""))):
        diagnostics.append("target_head must be an exact lowercase 40-hex commit SHA")

    contradictions = record.get("contradictions")
    if contradictions != []:
        diagnostics.append("contradictions must be an empty array")

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
    if event_sender != human_owner_login:
        diagnostics.append("receipt edit sender does not match configured Human Owner login")

    approval_time = _parse_time(record.get("approval_time"), "approval_time", diagnostics)
    if approval_time is not None:
        delta = abs((approval_event_time - approval_time).total_seconds())
        if delta > freshness_seconds:
            diagnostics.append(
                f"approval_time is not fresh for the receipt edit event ({delta:.0f}s delta)"
            )

    return GateResult(
        "PASS" if not diagnostics else "HOLD",
        tuple(diagnostics),
        expected_pr,
        expected_head,
    )


def validate_event(
    event: dict[str, Any],
    *,
    expected_repository: str,
    human_owner_login: str,
) -> GateResult:
    pull = event.get("pull_request")
    if not isinstance(pull, dict):
        return GateResult("HOLD", ("event does not contain a pull_request object",))
    base = pull.get("base") if isinstance(pull.get("base"), dict) else {}
    head = pull.get("head") if isinstance(pull.get("head"), dict) else {}
    sender = event.get("sender") if isinstance(event.get("sender"), dict) else {}
    expected_pr = event.get("number")
    expected_head = head.get("sha")
    expected_ref = pull.get("html_url")
    if base.get("ref") != "main":
        return GateResult("HOLD", ("target branch is not main",))
    if not isinstance(expected_pr, int) or not isinstance(expected_head, str) or not isinstance(expected_ref, str):
        return GateResult("HOLD", ("event target PR, exact head, or PR URL is missing",))
    event_time_diagnostics: list[str] = []
    event_time = _parse_time(pull.get("updated_at"), "pull_request.updated_at", event_time_diagnostics)
    if event_time is None:
        return GateResult("HOLD", tuple(event_time_diagnostics), expected_pr, expected_head)
    record, extract_error = _extract_receipt(pull.get("body"))
    if extract_error:
        return GateResult("HOLD", (extract_error,), expected_pr, expected_head)
    return validate_record(
        record,
        expected_repository=expected_repository,
        expected_pr=expected_pr,
        expected_head=expected_head,
        expected_ref=expected_ref,
        approval_event_time=event_time,
        event_action=str(event.get("action", "")),
        body_was_edited=isinstance(event.get("changes"), dict)
        and isinstance(event["changes"].get("body"), dict),
        event_sender=str(sender.get("login", "")),
        human_owner_login=human_owner_login,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed main-transition authority receipt gate")
    parser.add_argument("--github-event", type=Path, required=True)
    parser.add_argument("--expected-repository", required=True)
    parser.add_argument("--human-owner-login", required=True)
    args = parser.parse_args(argv)
    try:
        event = json.loads(args.github_event.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result = GateResult("HOLD", (f"event file is missing: {args.github_event}",))
    except json.JSONDecodeError as exc:
        result = GateResult("HOLD", (f"event JSON is invalid: {exc}",))
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
