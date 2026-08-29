from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from validate_main_transition_authority import BEGIN, END, SHA40, STATEMENT, validate_record


def build_receipt(
    *,
    repository: str,
    target_pr: int,
    target_head: str,
    approval_id: str,
    approval_time: datetime,
) -> dict[str, object]:
    pr_url = f"https://github.com/{repository}/pull/{target_pr}"
    return {
        "schema_version": "0.1.0",
        "record_type": "MAIN_TRANSITION_AUTHORITY_RECEIPT",
        "approval_id": approval_id,
        "repository": repository,
        "action": "MERGE_PR_INTO_MAIN",
        "target_branch": "main",
        "target_pr": target_pr,
        "target_head": target_head,
        "approval_time": approval_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "human_owner_explicit_approval": "GIVEN",
        "explicit_statement": STATEMENT,
        "approval_source": {
            "kind": "GITHUB_PR_BODY_EDIT",
            "ref": pr_url,
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


def render_receipt(record: dict[str, object]) -> str:
    return f"{BEGIN}\n```json\n{json.dumps(record, ensure_ascii=False, indent=2)}\n```\n{END}\n"


def parse_approval_time(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("approval time must include an explicit timezone")
    return parsed.astimezone(timezone.utc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate and self-check a main-transition authority receipt block"
    )
    parser.add_argument("--repository", default="maker-luder/aion-governance-framework")
    parser.add_argument("--pr", type=int, required=True, dest="target_pr")
    parser.add_argument("--head", required=True, dest="target_head")
    parser.add_argument("--approval-id", default=None)
    parser.add_argument("--approval-time", default=None)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    if args.target_pr < 1:
        parser.error("--pr must be a positive integer")
    if not SHA40.fullmatch(args.target_head):
        parser.error("--head must be an exact lowercase 40-hex commit SHA")
    if args.repository.count("/") != 1 or any(
        not part.strip() for part in args.repository.split("/")
    ):
        parser.error("--repository must use owner/name form")

    try:
        approval_time = parse_approval_time(args.approval_time)
        approval_id = str(uuid.UUID(args.approval_id)) if args.approval_id else str(uuid.uuid4())
    except ValueError as exc:
        parser.error(str(exc))

    record = build_receipt(
        repository=args.repository,
        target_pr=args.target_pr,
        target_head=args.target_head,
        approval_id=approval_id,
        approval_time=approval_time,
    )
    pr_url = f"https://github.com/{args.repository}/pull/{args.target_pr}"
    self_check = validate_record(
        record,
        expected_repository=args.repository,
        expected_pr=args.target_pr,
        expected_head=args.target_head,
        expected_ref=pr_url,
        approval_event_time=approval_time,
        event_action="edited",
        body_was_edited=True,
        event_sender="HUMAN_OWNER",
        human_owner_login="HUMAN_OWNER",
    )
    if self_check.status != "PASS":
        parser.error(f"generated receipt failed self-check: {self_check.diagnostics}")

    rendered = render_receipt(record)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
