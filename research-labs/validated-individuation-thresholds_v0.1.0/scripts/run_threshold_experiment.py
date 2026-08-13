from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from aion_individuation_thresholds import (
    BoundaryPerturbation,
    CriterionKind,
    CriterionObservation,
    CriterionSpec,
    IndividuationProfile,
    ThresholdDirection,
    audit_individuation_profile,
)


REGISTRATION = "2026-01-01T00:00:00+00:00"
START = "2026-01-02T00:00:00+00:00"
END = "2026-01-03T00:00:00+00:00"


def criterion(criterion_id: str, kind: CriterionKind, threshold: float = 0.8) -> CriterionSpec:
    return CriterionSpec(
        criterion_id=criterion_id,
        kind=kind,
        threshold=threshold,
        direction=ThresholdDirection.AT_LEAST,
        preregistration_ref=f"prereg:{criterion_id}",
        measurement_ref=f"measurement:{criterion_id}",
    )


def observation(criterion_id: str, context_id: str, value: float = 0.9) -> CriterionObservation:
    return CriterionObservation(
        criterion_id=criterion_id,
        context_id=context_id,
        observed_at="2026-01-02T12:00:00+00:00",
        value=value,
        source_ref=f"source:{criterion_id}:{context_id}",
    )


def base_profile(**changes: object) -> IndividuationProfile:
    values: dict[str, object] = {
        "profile_id": "profile-exp",
        "target_ref": "target:synthetic",
        "protocol_version": "individuation-protocol-v0.1.0",
        "registration_ref": "registration:synthetic",
        "registration_hash": "sha256:synthetic",
        "registration_timestamp": REGISTRATION,
        "observation_start": START,
        "observation_end": END,
        "criteria": (
            criterion("temporal", CriterionKind.TEMPORAL_INTEGRITY),
            criterion("boundary", CriterionKind.BOUNDARY_COHERENCE),
        ),
        "observations": (
            observation("temporal", "ctx-a"),
            observation("temporal", "ctx-b", 0.85),
            observation("boundary", "ctx-a", 0.88),
            observation("boundary", "ctx-b", 0.81),
        ),
        "contexts": ("ctx-a", "ctx-b"),
        "required_context_count": 2,
        "perturbations": (
            BoundaryPerturbation(
                perturbation_id="perturbation-1",
                variable_ref="boundary-variable:1",
                alteration_ref="alteration:remove-context",
                expected_boundary_test_ref="expected-test:boundary",
            ),
        ),
        "identity_claim": "NOT_ESTABLISHED",
        "contradiction_refs": (),
        "thresholds_locked": True,
    }
    values.update(changes)
    return IndividuationProfile(**values)


def build_cases() -> list[tuple[str, IndividuationProfile]]:
    unstable = list(base_profile().observations)
    unstable[-1] = observation("boundary", "ctx-b", 0.3)
    executed = replace(base_profile().perturbations[0], observed=True)
    return [
        ("valid-review-only", base_profile()),
        ("post-hoc-thresholds", base_profile(thresholds_locked=False)),
        ("registration-after-observation", base_profile(registration_timestamp=START)),
        ("cross-context-instability", base_profile(observations=tuple(unstable))),
        ("contradictory-profile", base_profile(contradiction_refs=("profile:other",))),
        ("missing-perturbation-metadata", base_profile(perturbations=())),
        ("executed-perturbation", base_profile(perturbations=(executed,))),
        ("identity-request", base_profile(identity_claim="IDENTITY_ESTABLISHED")),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for case_id, profile in build_cases():
        decision = audit_individuation_profile(profile)
        records.append(
            {
                "case_id": case_id,
                "decision": decision.as_dict(),
            }
        )
    payload = {
        "schema_version": "0.1.0",
        "experiment": "validated-individuation-thresholds-synthetic-audit",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "threshold_validated": False,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
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
