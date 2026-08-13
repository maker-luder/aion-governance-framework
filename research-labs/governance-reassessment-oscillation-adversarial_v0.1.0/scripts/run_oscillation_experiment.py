from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_governance_oscillation import (
    EvidenceLevel,
    EvidenceStatus,
    EventDirection,
    ReassessmentEvent,
    ReassessmentSequence,
    audit_reassessment_sequence,
)


def event(event_id: str, index: int, level: EvidenceLevel, direction: EventDirection, *, status: EvidenceStatus = EvidenceStatus.CURRENT, source: str | None = "source:1", provenance: str | None = "prov:1", interpretation: str | None = "interpretation:review", reason: str = "declared review transition", scope: str = "scope:bounded", counterevidence: tuple[str, ...] = (), stale_basis: str | None = None, correction: str | None = None) -> ReassessmentEvent:
    return ReassessmentEvent(
        event_id=event_id,
        sequence_index=index,
        observed_level=level,
        evidence_status=status,
        direction=direction,
        source_ref=source,
        provenance_ref=provenance,
        interpretation_ref=interpretation,
        reason=reason,
        claim_scope=scope,
        counterevidence_refs=counterevidence,
        stale_basis_ref=stale_basis,
        correction_ref=correction,
        trigger_ref="trigger:review",
    )


def sequence(*events: ReassessmentEvent, **changes: object) -> ReassessmentSequence:
    values: dict[str, object] = {
        "sequence_id": "sequence:oscillation-exp",
        "events": events,
        "initial_level": EvidenceLevel.E1,
        "preregistration_ref": "preregistration:reassessment-1",
        "currentness_policy_ref": "policy:currentness-1",
        "hysteresis_policy_ref": "policy:hysteresis-1",
        "human_review_required": True,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }
    values.update(changes)
    return ReassessmentSequence(**values)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, ReassessmentSequence]] = [
        ("stable", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), event("event:2", 2, EvidenceLevel.E2, EventDirection.STABLE))),
        ("oscillatory", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), event("event:2", 2, EvidenceLevel.E3, EventDirection.UP), event("event:3", 3, EvidenceLevel.E2, EventDirection.DOWN), event("event:4", 4, EvidenceLevel.E3, EventDirection.UP))),
        ("single-reversal", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), event("event:2", 2, EvidenceLevel.E3, EventDirection.UP), event("event:3", 3, EvidenceLevel.E2, EventDirection.DOWN))),
        ("stale-reviewed", sequence(event("event:stale", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.STALE, stale_basis="basis:stale", correction="correction:1"))),
        ("stale-reversal-no-correction", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), event("event:stale", 2, EvidenceLevel.E1, EventDirection.DOWN, status=EvidenceStatus.STALE, stale_basis="basis:stale"))),
        ("stale-no-basis", sequence(event("event:stale", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.STALE))),
        ("contradictory-reviewed", sequence(event("event:contradictory", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.CONTRADICTORY, counterevidence=("counter:1",), correction="correction:1"))),
        ("contradictory-no-counterevidence", sequence(event("event:contradictory", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.CONTRADICTORY, correction="correction:1"))),
        ("unknown-currentness", sequence(event("event:unknown", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.UNKNOWN))),
        ("missing-provenance", sequence(event("event:missing", 1, EvidenceLevel.E2, EventDirection.UP, source=None))),
        ("direction-mismatch", sequence(event("event:bad", 1, EvidenceLevel.E2, EventDirection.DOWN))),
        ("duplicate-sequence-index", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), event("event:2", 1, EvidenceLevel.E3, EventDirection.UP))),
        ("policy-metadata-missing", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), hysteresis_policy_ref=None)),
        ("boundary-effect", sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), canonical_effect="WRITE", governance_effect="PROMOTE", deployment=True)),
    ]
    records = []
    for case_id, item in cases:
        decision = audit_reassessment_sequence(item)
        records.append({"case_id": case_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "governance-reassessment-oscillation-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
