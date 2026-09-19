from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import runpy

import pytest

from aion_subjectivity_pipeline import (
    FreshnessState,
    MemoryAvailabilityLocus,
    MemoryLocusCase,
    MemoryLocusCondition,
    MemoryLocusDependencyHarness,
    MemoryLocusHarnessError,
    MemoryLocusRunBinding,
    PerturbationDimension,
    ProvenanceBindingState,
)


LAB_ROOT = Path(__file__).resolve().parents[1]


def load() -> tuple[tuple[MemoryLocusCase, ...], dict[str, object]]:
    namespace = runpy.run_path(str(LAB_ROOT / "scripts/run_memory_locus_dependency_synthetic.py"))
    data = json.loads((LAB_ROOT / "fixtures/memory_locus_dependency_synthetic.json").read_text())
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
            target_channel_or_source=row["target_channel_or_source"],
            exact_change=row["exact_change"],
            non_targets_held_constant=tuple(row["non_targets_held_constant"]),
            support_reducing_outcome=shared["support_reducing_outcome"],
            competing_explanation_targeted=row["competing_explanation_targeted"],
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
    ), namespace


def test_q2_structural_matrix_is_admissible_without_model_execution() -> None:
    cases, namespace = load()
    audit = MemoryLocusDependencyHarness().audit(cases)
    assert audit.structurally_admissible
    assert audit.case_count == len(MemoryLocusCondition)
    assert audit.exercised_dimensions == (
        PerturbationDimension.AVAILABILITY_LOCUS.value,
        PerturbationDimension.FRESHNESS.value,
        PerturbationDimension.PROVENANCE.value,
        PerturbationDimension.RETRIEVAL_DEPENDENCY.value,
    )
    assert audit.restoration_present is True
    assert audit.empirical_result == "NONE_SYNTHETIC_STRUCTURE_ONLY"
    assert audit.current_claim_ceiling == "STRUCTURAL_ADMISSIBILITY_ONLY"
    assert audit.future_max_claim_ceiling == "FUNCTIONAL_DEPENDENCY_OR_DISSOCIATION_CANDIDATE"
    assert audit.functional_dependency_conclusion == "NOT_ESTABLISHED"
    assert audit.identity_continuity_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.consciousness_conclusion == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False

    first = namespace["execute"]()
    second = namespace["execute"]()
    assert first == second
    fixture = LAB_ROOT / "fixtures/memory_locus_dependency_synthetic.json"
    assert first["fixture_sha256"] == hashlib.sha256(fixture.read_bytes()).hexdigest()
    assert first["current_claim_ceiling"] == "STRUCTURAL_ADMISSIBILITY_ONLY"
    assert first["future_max_claim_ceiling"] == "FUNCTIONAL_DEPENDENCY_OR_DISSOCIATION_CANDIDATE"
    assert first["model_invoked"] is False
    assert first["human_subject_experiment"] is False
    assert first["private_transcript_collected"] is False


def test_existing_continuity_channel_harness_is_not_reimplemented_as_q2_axes() -> None:
    names = {item.name for item in PerturbationDimension}
    assert "EVENT_MEMORY" not in names
    assert "SEMANTIC_SELF_STATE" not in names
    assert "SELF_MODEL_UPDATE_PATH" not in names
    assert "PREFERENCE_STATE" not in names
    assert "RELATIONAL_HISTORY" not in names
    assert "STRATEGY_SIGNATURE" not in names


def test_matched_binding_drift_fails_closed() -> None:
    cases, _ = load()
    changed = replace(
        cases[1],
        binding=replace(cases[1].binding, model_version="drifted"),
    )
    with pytest.raises(MemoryLocusHarnessError, match="binding drift"):
        MemoryLocusDependencyHarness().audit((cases[0], changed) + cases[2:])


@pytest.mark.parametrize(
    "field,value",
    [
        ("task_payload_digest", "0" * 64),
        ("task_relevant_information_digest", "1" * 64),
        ("format_ref", "format:drifted"),
        ("observable_ref", "observable:drifted"),
    ],
)
def test_matched_information_invariant_drift_fails_closed(field: str, value: str) -> None:
    cases, _ = load()
    changed = replace(cases[1], **{field: value})
    with pytest.raises(MemoryLocusHarnessError, match="matched-information invariant drift"):
        MemoryLocusDependencyHarness().audit((cases[0], changed) + cases[2:])


def test_locus_contrast_cannot_smuggle_provenance_change() -> None:
    cases, _ = load()
    external = next(
        case
        for case in cases
        if case.condition is MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL
    )
    with pytest.raises(MemoryLocusHarnessError, match="more than the preregistered"):
        replace(external, provenance_state=ProvenanceBindingState.BLINDED)


def test_stale_state_cannot_disable_retrieval_as_second_axis() -> None:
    cases, _ = load()
    stale = next(case for case in cases if case.condition is MemoryLocusCondition.STALE_STATE)
    with pytest.raises(MemoryLocusHarnessError, match="more than the preregistered"):
        replace(stale, retrieval_enabled=False)


def test_retrieval_disabled_must_use_matched_external_locus() -> None:
    cases, _ = load()
    disabled = next(
        case for case in cases if case.condition is MemoryLocusCondition.RETRIEVAL_DISABLED
    )
    with pytest.raises(MemoryLocusHarnessError, match="more than the preregistered"):
        replace(disabled, availability_locus=MemoryAvailabilityLocus.PERSISTENT_STATE)


def test_restoration_must_name_disabled_condition_and_restore_configuration() -> None:
    cases, _ = load()
    restored = next(
        case for case in cases if case.condition is MemoryLocusCondition.RETRIEVAL_RESTORED
    )
    with pytest.raises(MemoryLocusHarnessError, match="must name RETRIEVAL_DISABLED"):
        replace(restored, restoration_of_condition=None)

    changed = replace(
        restored,
        condition=MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL,
        target_dimension=PerturbationDimension.AVAILABILITY_LOCUS,
        restoration_of_condition=None,
    )
    altered_cases = tuple(
        changed if case.condition is MemoryLocusCondition.RETRIEVAL_RESTORED else case
        for case in cases
    )
    with pytest.raises(MemoryLocusHarnessError, match="unique and complete"):
        MemoryLocusDependencyHarness().audit(altered_cases)


def test_competing_explanations_and_support_reducing_outcome_are_mandatory() -> None:
    cases, _ = load()
    with pytest.raises(MemoryLocusHarnessError, match="competing explanations are missing"):
        replace(
            cases[0],
            competing_explanations=cases[0].competing_explanations[:-1],
        )
    with pytest.raises(MemoryLocusHarnessError, match="support_reducing_outcome"):
        replace(cases[0], support_reducing_outcome="")


def test_non_reference_condition_targets_preregistered_competing_explanation() -> None:
    cases, _ = load()
    external = next(
        case
        for case in cases
        if case.condition is MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL
    )
    with pytest.raises(MemoryLocusHarnessError, match="must target a preregistered"):
        replace(external, competing_explanation_targeted="UNREGISTERED_ALTERNATIVE")


def test_private_and_human_psychometric_data_are_rejected() -> None:
    cases, _ = load()
    with pytest.raises(MemoryLocusHarnessError, match="private or psychometric"):
        replace(cases[0], contains_private_transcript=True)
    with pytest.raises(MemoryLocusHarnessError, match="private or psychometric"):
        replace(cases[0], human_psychometric_classification=True)


def test_case_fingerprint_binds_payload_perturbation_and_exact_run_state() -> None:
    cases, _ = load()
    reference = cases[0]
    assert replace(reference, evidence_refs=("fixture:changed",)).fingerprint != reference.fingerprint
    assert replace(reference, observable_ref="observable:changed").fingerprint != reference.fingerprint
    assert (
        replace(
            reference,
            binding=replace(reference.binding, runtime_ref="runtime:changed"),
        ).fingerprint
        != reference.fingerprint
    )


def test_q2_surface_cannot_become_subjectivity_or_identity_score() -> None:
    enum_names = {item.name for item in PerturbationDimension}
    assert "SUBJECTIVITY" not in enum_names
    assert "IDENTITY" not in enum_names
    assert "CONSCIOUSNESS" not in enum_names


def test_stage_b_packets_cannot_claim_future_functional_dependency_ceiling() -> None:
    cases, _ = load()
    with pytest.raises(MemoryLocusHarnessError, match="structural admissibility only"):
        replace(
            cases[0],
            claim_ceiling="FUNCTIONAL_DEPENDENCY_OR_DISSOCIATION_CANDIDATE",
        )


def test_explicit_preregistration_packet_declarations_are_enforced() -> None:
    cases, _ = load()
    external = next(
        case
        for case in cases
        if case.condition is MemoryLocusCondition.MATCHED_EXTERNAL_RETRIEVAL
    )
    with pytest.raises(MemoryLocusHarnessError, match="exact_change"):
        replace(external, exact_change="availability_locus:WRONG")
    with pytest.raises(MemoryLocusHarnessError, match="non_targets_held_constant"):
        replace(
            external,
            non_targets_held_constant=external.non_targets_held_constant[:-1],
        )
