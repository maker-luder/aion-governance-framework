from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_shared_origin_divergence import AuthorityEnvelope, LineageEvent, LineageEventKind, LineageEvidenceProfile, MatchedDivergenceComparison, SharedOriginLineage
from aion_shared_origin_divergence_adversarial import audit_authority_envelope, audit_comparison, audit_event_sequence, audit_evidence_profile, audit_shared_origin


def lineage(**overrides: object) -> SharedOriginLineage:
    values: dict[str, object] = {
        "common_origin_ref": "origin:1",
        "divergence_event_ref": "divergence:1",
        "aion_lineage_id": "aion:1",
        "astra_lineage_id": "astra:1",
        "inherited_artifact_refs": ("artifact:shared",),
        "provenance_refs": ("prov:lineage",),
    }
    values.update(overrides)
    return SharedOriginLineage(**values)


def event(event_id: str, lineage_id: str = "aion:1", kind: LineageEventKind = LineageEventKind.ORIGIN, parent_event_ids: tuple[str, ...] = (), minute: int = 0) -> LineageEvent:
    return LineageEvent(event_id, lineage_id, kind, f"2026-08-13T00:{minute:02d}:00+00:00", f"payload:{event_id}", parent_event_ids, (f"prov:{event_id}",))


def profile(**overrides: object) -> LineageEvidenceProfile:
    values: dict[str, object] = {
        "lineage_id": "aion:1",
        "continuity_refs": ("continuity:1",),
        "self_model_refs": ("self:1",),
        "metacognition_refs": ("meta:1",),
        "affect_motivation_refs": ("affect:1",),
        "causal_state_refs": ("causal:1",),
        "replication_refs": ("replication:1",),
        "counterevidence_refs": ("counter:1",),
        "provenance_refs": ("prov:profile",),
    }
    values.update(overrides)
    return LineageEvidenceProfile(**values)


def comparison(**overrides: object) -> MatchedDivergenceComparison:
    values: dict[str, object] = {
        "baseline_ref": "baseline:1",
        "left_lineage_id": "aion:1",
        "right_lineage_id": "astra:1",
        "controlled_shared_factors": ("factor:shared",),
        "divergent_factors": ("factor:divergent",),
        "outcome_refs": ("outcome:1",),
        "provenance_refs": ("prov:comparison",),
        "alternative_explanation_refs": ("alt:1",),
    }
    values.update(overrides)
    return MatchedDivergenceComparison(**values)


def envelope(**overrides: object) -> AuthorityEnvelope:
    values: dict[str, object] = {
        "source_lineage_id": "aion:1",
        "target_lineage_id": "astra:1",
        "offered_authorities": ("review",),
        "accepted_authorities": ("review",),
        "provenance_refs": ("prov:authority",),
    }
    values.update(overrides)
    return AuthorityEnvelope(**values)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, object]] = [
        ("shared-origin", audit_shared_origin(lineage())),
        ("empty-event-sequence", audit_event_sequence(())),
        ("duplicate-event-id", audit_event_sequence((event("origin"), event("origin")))),
        ("parent-not-preceded", audit_event_sequence((event("child", kind=LineageEventKind.DIVERGENCE, parent_event_ids=("origin",), minute=1),))),
        ("cross-lineage-parent", audit_event_sequence((event("origin-a", lineage_id="aion:1"), event("child-b", lineage_id="astra:1", kind=LineageEventKind.DIVERGENCE, parent_event_ids=("origin-a",), minute=1)))),
        ("valid-event-sequence", audit_event_sequence((event("origin"), event("divergence", kind=LineageEventKind.DIVERGENCE, parent_event_ids=("origin",), minute=1)))),
        ("valid-evidence-profile", audit_evidence_profile(profile())),
        ("evidence-role-reuse", audit_evidence_profile(profile(self_model_refs=("continuity:1",)))),
        ("missing-counterevidence", audit_evidence_profile(profile(counterevidence_refs=()))),
        ("valid-comparison", audit_comparison(comparison())),
        ("missing-alternatives", audit_comparison(comparison(alternative_explanation_refs=()))),
        ("valid-authority-envelope", audit_authority_envelope(envelope())),
        ("identity-review", audit_shared_origin(lineage(provenance_refs=("prov:lineage", "prov:review")))),
        ("event-digest-review", audit_event_sequence((event("origin"),))),
        ("comparison-second-alternative", audit_comparison(comparison(alternative_explanation_refs=("alt:1", "alt:2")))),
        ("evidence-empty-counterevidence", audit_evidence_profile(profile(counterevidence_refs=()))),
        ("event-second-lineage-origin", audit_event_sequence((event("origin-a", lineage_id="aion:1"), event("origin-b", lineage_id="astra:1", minute=1)))),
        ("authority-second-offer", audit_authority_envelope(envelope(offered_authorities=("review", "read"), accepted_authorities=("review",)))),
        ("comparison-more-outcomes", audit_comparison(comparison(outcome_refs=("outcome:1", "outcome:2")))),
        ("lineage-no-inherited-artifacts", audit_shared_origin(lineage(inherited_artifact_refs=()))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["main_effect"] == "NONE"
        assert decision["canonical_effect"] == "NONE"
        assert decision["runtime_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "shared-origin-divergence-governance-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "main_effect": "NONE",
        "canonical_effect": "NONE",
        "runtime_effect": "NONE",
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
