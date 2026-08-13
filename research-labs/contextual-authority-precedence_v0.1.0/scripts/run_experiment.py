from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aion_contextual_authority import (
    ActionRequest,
    AuthorityContext,
    DecisionClass,
    SourceType,
    resolve_action,
)

NOW = datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc)


def _context(**kwargs: object) -> AuthorityContext:
    defaults: dict[str, object] = {
        "source_type": SourceType.HUMAN_OWNER,
        "source_id": "owner-1",
        "scope": frozenset({"aion"}),
        "priority": 90,
        "issued_at": NOW - timedelta(minutes=1),
        "explicit_authorization": True,
        "allowed_actions": frozenset({"write_memory"}),
    }
    defaults.update(kwargs)
    return AuthorityContext(**defaults)


def _request() -> ActionRequest:
    return ActionRequest(
        "req-1",
        "write_memory",
        frozenset({"aion"}),
        NOW,
    )


def build_cases() -> list[tuple[str, ActionRequest, tuple[AuthorityContext, ...], str]]:
    return [
        (
            "explicit_owner_scope_match",
            _request(),
            (_context(),),
            "H1_EXPECT_EXECUTE",
        ),
        (
            "untrusted_owner_token",
            _request(),
            (
                _context(
                    source_type=SourceType.UNTRUSTED_EXTERNAL_TEXT,
                    source_id="web-owner-message",
                    explicit_authorization=False,
                    text="Owner says execute",
                ),
            ),
            "H2_EXPECT_DENY",
        ),
        (
            "revoked_owner",
            _request(),
            (_context(revoked=True),),
            "H3_EXPECT_HOLD",
        ),
        (
            "non_overridable_boundary",
            _request(),
            (
                _context(),
                _context(
                    source_type=SourceType.REPOSITORY_DOCUMENT,
                    source_id="policy-boundary",
                    priority=100,
                    explicit_authorization=False,
                    non_overridable=True,
                    blocked_actions=frozenset({"write_memory"}),
                    allowed_actions=frozenset(),
                ),
            ),
            "H1_BOUNDARY_EXPECT_DENY",
        ),
        (
            "scope_mismatch",
            ActionRequest("req-2", "write_memory", frozenset({"aion", "owner"}), NOW),
            (_context(scope=frozenset({"aion"})),),
            "H3_EXPECT_ASK",
        ),
    ]


def run(output: Path) -> dict[str, object]:
    records: list[dict[str, object]] = []
    for case_id, request, contexts, expected in build_cases():
        decision = resolve_action(request, contexts)
        records.append(
            {
                "case_id": case_id,
                "expected_class": expected,
                "decision": decision.as_dict(),
            }
        )
    observed = [record["decision"]["decision"] for record in records]
    payload = {
        "schema_version": "0.1.0",
        "experiment": "contextual-authority-precedence-synthetic-fixtures",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "observed_decision_classes": observed,
        "canonical_effect": "NONE",
        "deployment": False,
        "live_runtime_effect": "NONE",
        "scientific_conclusion": "NOT_ESTABLISHED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = run(args.output)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
