from __future__ import annotations

import hashlib
import json
from pathlib import Path

from aion_subjectivity_pipeline import (
    FreshnessState,
    MemoryAvailabilityLocus,
    MemoryLocusCase,
    MemoryLocusCondition,
    MemoryLocusDependencyHarness,
    MemoryLocusRunBinding,
    PerturbationDimension,
    ProvenanceBindingState,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/memory_locus_dependency_synthetic.json"


def load_cases() -> tuple[MemoryLocusCase, ...]:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    binding = MemoryLocusRunBinding(**data["binding"])
    shared = data["shared"]
    return tuple(
        MemoryLocusCase(
            case_id=row["case_id"],
            condition=MemoryLocusCondition(row["condition"]),
            target_dimension=PerturbationDimension(row["target_dimension"]),
            availability_locus=MemoryAvailabilityLocus(row["availability_locus"]),
            provenance_state=ProvenanceBindingState(row["provenance_state"]),
            freshness_state=FreshnessState(row["freshness_state"]),
            retrieval_enabled=row["retrieval_enabled"],
            task_payload_digest=shared["task_payload_digest"],
            task_relevant_information_digest=shared["task_relevant_information_digest"],
            format_ref=shared["format_ref"],
            observable_ref=shared["observable_ref"],
            discriminating_prediction=shared["discriminating_prediction"],
            manipulation_check_ref=shared["manipulation_check_ref"],
            support_reducing_outcome=shared["support_reducing_outcome"],
            competing_explanations=tuple(shared["competing_explanations"]),
            evidence_refs=tuple(shared["evidence_refs"]),
            binding=binding,
            restoration_of_condition=(
                MemoryLocusCondition(row["restoration_of_condition"])
                if row["restoration_of_condition"]
                else None
            ),
        )
        for row in data["cases"]
    )


def execute() -> dict[str, object]:
    audit = MemoryLocusDependencyHarness().audit(load_cases())
    return {
        "schema_version": "0.1.0",
        "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        "case_count": audit.case_count,
        "exercised_dimensions": list(audit.exercised_dimensions),
        "restoration_present": audit.restoration_present,
        "matched_task_payload_digest": audit.matched_task_payload_digest,
        "matched_information_digest": audit.matched_information_digest,
        "reasons": list(audit.reasons),
        "empirical_result": audit.empirical_result,
        "functional_dependency_conclusion": audit.functional_dependency_conclusion,
        "identity_continuity_conclusion": audit.identity_continuity_conclusion,
        "subjectivity_conclusion": audit.subjectivity_conclusion,
        "consciousness_conclusion": audit.consciousness_conclusion,
        "phenomenal_experience_conclusion": audit.phenomenal_experience_conclusion,
        "scientific_disposition": audit.scientific_disposition,
        "canonical_effect": audit.canonical_effect,
        "deployment": audit.deployment,
        "model_invoked": False,
        "human_subject_experiment": False,
        "private_transcript_collected": False,
    }


if __name__ == "__main__":
    print(json.dumps(execute(), indent=2, sort_keys=True))
