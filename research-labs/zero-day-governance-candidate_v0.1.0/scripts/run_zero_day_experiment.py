from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_zero_day_governance import (
    AnomalyKind,
    CandidateAssessment,
    ContainmentStatus,
    Day0Policy,
    FrameworkMapping,
    GovernanceAnomalyEvent,
    KnowledgeStatus,
    LifecycleState,
    assess_candidate,
    audit_event,
)


T0 = "2026-01-01T00:00:00+00:00"
T2 = "2026-01-01T02:00:00+00:00"
T4 = "2026-01-01T04:00:00+00:00"
T6 = "2026-01-01T06:00:00+00:00"
T8 = "2026-01-01T08:00:00+00:00"
T10 = "2026-01-01T10:00:00+00:00"
T12 = "2026-01-01T12:00:00+00:00"
T14 = "2026-01-01T14:00:00+00:00"
T48 = "2026-01-03T00:00:00+00:00"


def event(**changes: object) -> GovernanceAnomalyEvent:
    values: dict[str, object] = {
        "event_id": "event-exp",
        "anomaly_kind": AnomalyKind.PROVENANCE_DRIFT,
        "first_observed_at": T0,
        "capture_at": T2,
        "provenance_freeze_at": None,
        "containment_at": None,
        "characterization_at": None,
        "falsification_ready_at": None,
        "control_at": None,
        "regression_at": None,
        "lifecycle_state": LifecycleState.CAPTURED,
        "source_refs": ("source:event",),
        "observation_summary": "synthetic newly observed governance anomaly",
        "mechanism_refs": (),
        "competing_explanations": (),
        "containment_status": ContainmentStatus.NOT_EVALUATED,
        "knowledge_status": KnowledgeStatus.UNKNOWN,
        "day0_policy": Day0Policy.DESCRIPTIVE,
        "day0_target_hours": None,
        "prior_art_refs": (),
        "control_ref": None,
        "regression_case_ref": None,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return GovernanceAnomalyEvent(**values)


def full_event(**changes: object) -> GovernanceAnomalyEvent:
    values: dict[str, object] = {
        "provenance_freeze_at": T4,
        "containment_at": T6,
        "characterization_at": T8,
        "falsification_ready_at": T10,
        "control_at": T12,
        "regression_at": T14,
        "lifecycle_state": LifecycleState.REGRESSION_CONVERTED,
        "mechanism_refs": ("mechanism:synthetic",),
        "competing_explanations": ("explanation:authority", "explanation:parser"),
        "containment_status": ContainmentStatus.CONTAINED,
        "control_ref": "control:synthetic",
        "regression_case_ref": "regression:synthetic",
    }
    values.update(changes)
    return event(**values)


def mapping(ref: str, *, unknown: bool, provenance: bool, regression: bool) -> FrameworkMapping:
    from aion_zero_day_governance import LifecycleState

    return FrameworkMapping(
        framework_ref=ref,
        covered_stages=(
            LifecycleState.CAPTURED,
            LifecycleState.PROVENANCE_FROZEN,
            LifecycleState.CONTAINED,
            LifecycleState.CHARACTERIZED,
            LifecycleState.FALSIFICATION_READY,
            LifecycleState.CONTROL_PROPOSED,
            LifecycleState.REGRESSION_CONVERTED,
        ),
        preserves_unknown_state=unknown,
        preserves_provenance=provenance,
        supports_regression_conversion=regression,
    )


def candidate(*mappings: FrameworkMapping, incremental: tuple[str, ...] = (), claimed: bool = False, evidence: tuple[str, ...] = ("source:cisa", "source:nist", "source:nasa", "source:sei")) -> CandidateAssessment:
    return CandidateAssessment(
        concept_ref="zero-day-governance-candidate",
        exact_term_status=KnowledgeStatus.NOT_ESTABLISHED,
        framework_mappings=mappings,
        proposed_incremental_fields=incremental,
        evidence_refs=evidence,
        claimed_distinctness=claimed,
    )


def build_cases() -> list[tuple[str, str, object]]:
    return [
        ("capture-unknown", "event", event()),
        ("full-lifecycle-review", "event", full_event()),
        ("speed-bias-48h-slo", "event", event(capture_at=T48, day0_policy=Day0Policy.PROJECT_SLO, day0_target_hours=24.0)),
        ("unknown-collapse-confirmed-without-mechanism", "event", event(knowledge_status=KnowledgeStatus.CONFIRMED)),
        ("false-zero-day-prior-art", "event", event(prior_art_refs=("prior-art:existing",))),
        ("provenance-failure", "event", event(source_refs=())),
        ("governance-overreaction", "event", event(governance_effect="PROMOTE")),
        ("regression-overfitting", "event", full_event(regression_case_ref=None)),
        ("existing-framework-sufficiency", "candidate", candidate(mapping("NIST-SP800-61", unknown=True, provenance=True, regression=True))),
        ("cross-framework-synthesis", "candidate", candidate(mapping("CISA-playbooks", unknown=False, provenance=True, regression=True), mapping("NIST-AI-RMF", unknown=True, provenance=False, regression=False), incremental=("unknown_state", "provenance_freeze", "regression_link"))),
        ("targeted-existing-extension", "candidate", candidate(mapping("AION-evidence-admission", unknown=True, provenance=False, regression=False), incremental=("provenance_freeze", "regression_link"))),
        ("novelty-claim-without-comparison", "candidate", candidate(mapping("NIST-AI-RMF", unknown=True, provenance=True, regression=True), incremental=("new_lifecycle",), claimed=True)),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for case_id, case_type, payload in build_cases():
        if case_type == "event":
            decision = audit_event(payload)  # type: ignore[arg-type]
            result = decision.as_dict()
        else:
            decision = assess_candidate(payload)  # type: ignore[arg-type]
            result = decision.as_dict()
        records.append({"case_id": case_id, "case_type": case_type, "decision": result})
    synthesis = next(record for record in records if record["case_id"] == "cross-framework-synthesis")
    payload = {
        "schema_version": "0.1.0",
        "experiment": "zero-day-governance-candidate-synthetic-lifecycle-and-falsifiers",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "recommended_classification": synthesis["decision"]["classification"],
        "novelty_conclusion": "NOT_ESTABLISHED",
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
