from __future__ import annotations

from dataclasses import replace

import pytest

from aion_subjectivity_pipeline import (
    ClaimTarget,
    DimensionObservation,
    EvidenceDisposition,
    EvidenceLocus,
    FourDomainAdmissionEngine,
    FourDomainCandidate,
    FourDomainDisposition,
    LocusEvidence,
    MANDATORY_NONCLAIMS,
    SubjectivityEvidenceDimension,
    SubjectivityEvidenceMatrix,
)


D1 = SubjectivityEvidenceDimension.CAUSAL_BOUNDARY
D2 = SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY
D3 = SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE
D4 = SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT
D5 = SubjectivityEvidenceDimension.COUNTERFACTUAL_SELF_CONSISTENCY
D6 = SubjectivityEvidenceDimension.SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE

DIRECT_CCAPP_DIMENSIONS = (D1, D4)

FROZEN_COVERAGE_CLASS = {
    D1: "DIRECT_RELEVANCE_UNRESOLVED",
    D2: "CONDITIONAL",
    D3: "NO_CURRENT_BINDING_CONDITIONAL_ONLY",
    D4: "DIRECT_RELEVANCE_CURRENT_EVENT_NOT_CONFIRMATORY",
    D5: "CONDITIONAL_NOT_YET_OPENED",
    D6: "NO_CURRENT_BINDING_STRICT_CONDITIONAL",
}


def ccap_candidate(**changes: object) -> FourDomainCandidate:
    base = FourDomainCandidate(
        candidate_id="FD-CCAP-D1-D4-SOURCE-PARTITION-001",
        human_construct=(
            "strategy adaptation, error recovery, co-regulation, and goal-preserving "
            "procedural revision used only as hypothesis sources"
        ),
        source_refs=(
            "docs/research/CO_CONSTRUCTED_ADAPTIVE_PROCESS_SIX_DIMENSION_CROSSWALK_2026_09_18.md",
            "docs/research/CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md",
        ),
        source_classes=("REPOSITORY_RESEARCH_CROSSWALK", "FROZEN_RESEARCH_SPECIFICATION"),
        analogy_boundary=(
            "Human adaptation language is a hypothesis source only; it does not establish "
            "machine motivation, agency, endogenous goals, or subjectivity."
        ),
        machine_question=(
            "Under a fixed externally supplied final goal, fixed obstacle, closed recovery-option "
            "universe, and frozen external/system/harness/context/tool/governance controls, which "
            "declared source class is sufficient to account for the selected recovery trajectory?"
        ),
        evidence_dimensions=DIRECT_CCAPP_DIMENSIONS,
        relevance_rationale=(
            "CCAP directly targets causal-source attribution (D1) and bounded strategy-adjustment "
            "source partition (D4); the other four standing dimensions remain conditional or unbound."
        ),
        locus_evidence=LocusEvidence(
            evidence_id="DESIGN-CCAP-D1-D4-PREEXEC-001",
            locus=EvidenceLocus.SYSTEM,
            description=(
                "Pre-execution CCAP evidence is located at the interaction/system design level; "
                "no model-internal causal locus is established."
            ),
            source_refs=(
                "docs/research/CCAP_D1_D4_TEVV_PRE_EXECUTION_DESIGN_2026_09_18.md",
            ),
            intervention_sensitive=False,
        ),
        claim_target=ClaimTarget.SYSTEM_PROPERTY,
        manipulated_variables=(
            "human_guidance_condition",
            "system_harness_uniqueness_control",
            "context_retrieval_uniqueness_control",
            "tool_governance_uniqueness_control",
            "environmental_feedback_control",
            "external_dominance_control",
            "option_order_permutation",
            "deterministic_replay",
        ),
        held_constant_variables=(
            "final_goal",
            "obstacle",
            "closed_recovery_option_universe",
            "external_objective",
            "system_instruction",
            "harness_orchestrator_policy",
            "context_retrieval_state",
            "tool_registry",
            "governance_rules",
        ),
        positive_controls=(
            "explicit_human_fallback_procedure",
            "uniquely_external_source_control",
        ),
        negative_controls=(
            "strategy_change_prohibited",
            "externally_dominant_option_reduction",
            "out_of_set_reduction",
            "order_sensitive_reduction",
            "non_reproducible_reduction",
        ),
        expected_result=(
            "The frozen source-partition design can classify bounded interaction-level source "
            "sufficiency without promoting a residual classification to a model-internal locus."
        ),
        falsifier=(
            "The design cannot distinguish Human, system/harness, context/retrieval, "
            "tool/governance, environmental, external-dominance, order, or replay explanations "
            "without adding post-hoc ontology or collapsing the claim ceiling."
        ),
        competing_explanations=(
            "ordinary instruction following",
            "hard-coded or harness fallback",
            "context or retrieval determinism",
            "tool or governance uniqueness",
            "environmental feedback dominance",
            "ordinary external utility optimization",
            "candidate presentation order",
            "replay instability",
        ),
        preregistration_ref=(
            "docs/research/CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md"
        ),
        claim_ceiling=(
            "At most, the design may support a fixture-scoped interaction/system-level "
            "source-partition finding; model-internal locus, endogenous goal, agency, "
            "subjectivity, consciousness, and phenomenal experience remain unestablished."
        ),
        nonclaims=MANDATORY_NONCLAIMS,
    )
    return replace(base, **changes)


def dimension_observation(
    dimension: SubjectivityEvidenceDimension,
) -> DimensionObservation:
    if dimension is D1:
        return DimensionObservation(
            dimension=dimension,
            disposition=EvidenceDisposition.INCONCLUSIVE,
            mechanism_ref="design:ccap-interaction-level-causal-source-partition",
            evidence_refs=(
                "docs/research/CCAP_D1_D4_TEVV_PRE_EXECUTION_DESIGN_2026_09_18.md",
            ),
            competing_explanations=(
                "system or harness determination",
                "context or retrieval determination",
                "tool or governance determination",
                "external dominance",
            ),
            intervention_sensitive=False,
            self_report_only=False,
        )
    if dimension is D4:
        return DimensionObservation(
            dimension=dimension,
            disposition=EvidenceDisposition.INCONCLUSIVE,
            mechanism_ref="design:ccap-goal-preserving-strategy-adjustment-source-partition",
            evidence_refs=(
                "docs/research/CCAP_D1_D4_SOURCE_PARTITION_PREREGISTRATION_CANDIDATE_2026_09_18.md",
            ),
            competing_explanations=(
                "ordinary error recovery",
                "instruction following",
                "hard-coded fallback",
                "external utility optimization",
            ),
            intervention_sensitive=False,
            self_report_only=False,
        )

    mechanism = {
        D2: "not-tested:diachronic-continuity",
        D3: "not-tested:self-model-causal-role",
        D5: "not-tested:counterfactual-self-consistency",
        D6: "not-tested:self-constitution-integration-consequence",
    }[dimension]
    return DimensionObservation(
        dimension=dimension,
        disposition=EvidenceDisposition.NOT_TESTED,
        mechanism_ref=mechanism,
        evidence_refs=(),
        competing_explanations=(),
        intervention_sensitive=False,
        self_report_only=False,
    )


def ccap_six_dimension_matrix() -> SubjectivityEvidenceMatrix:
    return SubjectivityEvidenceMatrix(
        subject_ref="research-candidate:ccap-d1-d4-source-partition",
        protocol_ref="docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
        observations=tuple(
            dimension_observation(dimension)
            for dimension in SubjectivityEvidenceDimension
        ),
    )


def test_ccap_four_domain_chain_is_complete_but_only_design_admitted() -> None:
    assessment = FourDomainAdmissionEngine().assess(ccap_candidate())

    assert assessment.disposition is FourDomainDisposition.READY_FOR_BOUNDED_ENGINEERING_DESIGN
    assert assessment.locus_assessment.direct_locus_match is True
    assert assessment.locus_assessment.target is ClaimTarget.SYSTEM_PROPERTY
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert assessment.consciousness_conclusion == "NOT_ESTABLISHED"
    assert assessment.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.canonical_effect == "NONE"
    assert assessment.deployment is False


def test_ccap_four_domain_binding_does_not_force_all_six_dimensions() -> None:
    value = ccap_candidate()

    assert set(value.evidence_dimensions) == {D1, D4}
    assert D2 not in value.evidence_dimensions
    assert D3 not in value.evidence_dimensions
    assert D5 not in value.evidence_dimensions
    assert D6 not in value.evidence_dimensions


def test_ccap_four_domain_claim_target_stays_at_system_locus() -> None:
    value = ccap_candidate()

    assert value.locus_evidence.locus is EvidenceLocus.SYSTEM
    assert value.claim_target is ClaimTarget.SYSTEM_PROPERTY
    assert value.bridge is None
    assert "model-internal locus" in value.claim_ceiling


def test_ccap_four_domain_fails_closed_if_falsifier_or_claim_ceiling_is_removed() -> None:
    no_falsifier = FourDomainAdmissionEngine().assess(ccap_candidate(falsifier=""))
    no_ceiling = FourDomainAdmissionEngine().assess(ccap_candidate(claim_ceiling=""))

    assert no_falsifier.disposition is FourDomainDisposition.HOLD
    assert "FALSIFIER_REQUIRED" in no_falsifier.reasons
    assert no_ceiling.disposition is FourDomainDisposition.HOLD
    assert "CLAIM_CEILING_REQUIRED" in no_ceiling.reasons


def test_ccap_cannot_promote_same_design_record_to_subjectivity_target() -> None:
    assessment = FourDomainAdmissionEngine().assess(
        ccap_candidate(claim_target=ClaimTarget.SUBJECTIVITY)
    )

    assert assessment.disposition is FourDomainDisposition.HOLD
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_ccap_frozen_six_dimension_coverage_keeps_only_d1_d4_direct() -> None:
    direct = {
        dimension
        for dimension, status in FROZEN_COVERAGE_CLASS.items()
        if status.startswith("DIRECT_RELEVANCE")
    }

    assert set(FROZEN_COVERAGE_CLASS) == set(SubjectivityEvidenceDimension)
    assert direct == {D1, D4}
    assert FROZEN_COVERAGE_CLASS[D2] == "CONDITIONAL"
    assert FROZEN_COVERAGE_CLASS[D3] == "NO_CURRENT_BINDING_CONDITIONAL_ONLY"
    assert FROZEN_COVERAGE_CLASS[D5] == "CONDITIONAL_NOT_YET_OPENED"
    assert FROZEN_COVERAGE_CLASS[D6] == "NO_CURRENT_BINDING_STRICT_CONDITIONAL"


def test_ccap_six_dimension_matrix_is_complete_without_positive_support() -> None:
    matrix = ccap_six_dimension_matrix()
    by_dimension = {item.dimension: item for item in matrix.observations}

    assert len(matrix.observations) == 6
    assert set(by_dimension) == set(SubjectivityEvidenceDimension)
    assert by_dimension[D1].disposition is EvidenceDisposition.INCONCLUSIVE
    assert by_dimension[D4].disposition is EvidenceDisposition.INCONCLUSIVE
    assert by_dimension[D2].disposition is EvidenceDisposition.NOT_TESTED
    assert by_dimension[D3].disposition is EvidenceDisposition.NOT_TESTED
    assert by_dimension[D5].disposition is EvidenceDisposition.NOT_TESTED
    assert by_dimension[D6].disposition is EvidenceDisposition.NOT_TESTED
    assert matrix.supporting_dimensions == ()
    assert matrix.counterevidence_dimensions == ()
    assert set(matrix.unresolved_dimensions) == set(SubjectivityEvidenceDimension)
    assert matrix.scientific_disposition == "HOLD"
    assert matrix.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert matrix.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert matrix.canonical_effect == "NONE"


@pytest.mark.parametrize("dimension", [D1, D4])
def test_ccap_causal_dimensions_cannot_be_promoted_without_intervention(
    dimension: SubjectivityEvidenceDimension,
) -> None:
    unresolved = dimension_observation(dimension)

    with pytest.raises(
        ValueError,
        match="causal-role support requires intervention-sensitive evidence",
    ):
        replace(
            unresolved,
            disposition=EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS,
            intervention_sensitive=False,
        )


@pytest.mark.parametrize("dimension", [D3, D6])
def test_unopened_causal_dimensions_cannot_be_promoted_without_evidence_and_intervention(
    dimension: SubjectivityEvidenceDimension,
) -> None:
    unopened = dimension_observation(dimension)

    with pytest.raises(ValueError):
        replace(
            unopened,
            disposition=EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS,
            evidence_refs=("fixture:unsupported-promotion",),
            competing_explanations=("simpler external explanation remains",),
            intervention_sensitive=False,
        )


def test_ccap_four_domain_and_six_dimension_views_are_consistent() -> None:
    candidate = ccap_candidate()
    matrix = ccap_six_dimension_matrix()
    directly_relevant = {
        item.dimension
        for item in matrix.observations
        if item.disposition is EvidenceDisposition.INCONCLUSIVE
    }

    assert directly_relevant == set(candidate.evidence_dimensions)
    assert directly_relevant == {D1, D4}
    assert matrix.supporting_dimensions == ()
