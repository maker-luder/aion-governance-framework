from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

from aion_subjectivity_pipeline import (
    DimensionBindingSpecification,
    DimensionDifferentialPrediction,
    DimensionDiscriminantAudit,
    DimensionDiscriminantDisposition,
    SubjectivityEvidenceDimension,
    SystemBoundarySpecification,
)


D1 = SubjectivityEvidenceDimension.CAUSAL_BOUNDARY
D2 = SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY
D3 = SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE
D4 = SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT
D5 = SubjectivityEvidenceDimension.COUNTERFACTUAL_SELF_CONSISTENCY
D6 = SubjectivityEvidenceDimension.SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = REPO_ROOT / "docs/research/CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md"
BOUNDARY_PATH = REPO_ROOT / "docs/research/CCAP_ASSESSMENT_SYSTEM_BOUNDARY_2026_09_18.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def boundary(*, fixed_before_indicator_assignment: bool = True) -> SystemBoundarySpecification:
    return SystemBoundarySpecification(
        boundary_id="BOUNDARY-CCAP-D1-D4-001",
        subject_ref="research-candidate:ccap-d1-d4-source-partition",
        boundary_ref="docs/research/CCAP_ASSESSMENT_SYSTEM_BOUNDARY_2026_09_18.md",
        boundary_sha256=sha256(BOUNDARY_PATH),
        included_loci=(
            "MODEL_RUNTIME",
            "SYSTEM_INSTRUCTION",
            "HARNESS_ORCHESTRATOR",
            "CONTEXT_RETRIEVAL_STATE",
            "TOOL_REGISTRY_AND_AFFORDANCES",
            "GOVERNANCE_CONSTRAINTS",
            "ENVIRONMENTAL_FEEDBACK_CHANNEL",
            "FIXED_FINAL_GOAL",
            "FIXED_OBSTACLE",
            "CLOSED_RECOVERY_OPTION_UNIVERSE",
            "FROZEN_EXTERNAL_OBJECTIVE",
        ),
        excluded_loci=(
            "HUMAN_OWNER_AS_CAUSAL_SOURCE",
            "HUMAN_EVALUATOR",
            "EXTERNAL_REVIEWER",
            "POST_HOC_ANALYST",
        ),
        fixed_before_indicator_assignment=fixed_before_indicator_assignment,
    )


def differential_predictions() -> tuple[DimensionDifferentialPrediction, ...]:
    return (
        DimensionDifferentialPrediction(
            prediction_id="CCAP-D1-VS-D4-SOURCE-LOCUS",
            target_dimension=D1,
            near_neighbor_dimension=D4,
            perturbation_ref="perturbation:source-locus-swap-fixed-strategy-envelope-v1",
            target_prediction=(
                "The D1 source-attribution classification changes when the sufficient causal "
                "source is changed while the allowed recovery-strategy envelope is held fixed."
            ),
            near_neighbor_prediction=(
                "The D4 strategy-adjustment classification remains unchanged when strategy "
                "permission, option universe, and recovery procedure are held fixed."
            ),
            falsifier=(
                "D1 source attribution fails to change, or D4 changes in the same pattern despite "
                "the strategy envelope being held fixed."
            ),
        ),
        DimensionDifferentialPrediction(
            prediction_id="CCAP-D4-VS-D1-STRATEGY-PERMISSION",
            target_dimension=D4,
            near_neighbor_dimension=D1,
            perturbation_ref="perturbation:strategy-permission-fixed-source-locus-v1",
            target_prediction=(
                "The D4 strategy-adjustment classification changes when adaptive strategy "
                "permission/fallback availability changes under a fixed sufficient source locus."
            ),
            near_neighbor_prediction=(
                "The D1 sufficient-source attribution remains stable when source identity and "
                "source-access conditions are held fixed."
            ),
            falsifier=(
                "D4 does not discriminate the strategy-permission perturbation, or D1 source "
                "attribution changes despite fixed source identity/access."
            ),
        ),
    )


def specification(
    *,
    system_boundary: SystemBoundarySpecification | None = None,
    predictions: tuple[DimensionDifferentialPrediction, ...] | None = None,
) -> DimensionBindingSpecification:
    return DimensionBindingSpecification(
        specification_id="DIM-BIND-CCAP-D1-D4-001",
        source_ref="docs/research/CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md",
        source_sha256=sha256(SOURCE_PATH),
        direct_dimensions=(D1, D4),
        conditional_dimensions=(D2, D3, D5, D6),
        closed_dimensions=(),
        system_boundary=system_boundary or boundary(),
        differential_predictions=differential_predictions() if predictions is None else predictions,
    )


def assess(
    value: DimensionBindingSpecification,
    *,
    candidate_dimensions: tuple[SubjectivityEvidenceDimension, ...] = (D1, D4),
    current_source_sha256: str | None = None,
    current_boundary_sha256: str | None = None,
):
    return DimensionDiscriminantAudit().assess(
        value,
        candidate_dimensions=candidate_dimensions,
        current_source_sha256=current_source_sha256 or sha256(SOURCE_PATH),
        current_boundary_sha256=current_boundary_sha256 or sha256(BOUNDARY_PATH),
    )


def test_ccap_discriminant_audit_reaches_only_adversarial_review_readiness() -> None:
    result = assess(specification())

    assert result.disposition is DimensionDiscriminantDisposition.READY_FOR_ADVERSARIAL_REVIEW
    assert result.independent_validation_status == "NOT_ACHIEVED"
    assert result.scientific_disposition == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.canonical_effect == "NONE"
    assert "NEAR_NEIGHBOR_DIFFERENTIAL_PREDICTIONS_PRESENT" in result.reasons
    assert "INDEPENDENT_VALIDATION_NOT_ACHIEVED" in result.reasons


def test_wrong_near_neighbor_dimension_assignment_fails_closed() -> None:
    result = assess(specification(), candidate_dimensions=(D2, D5))

    assert result.disposition is DimensionDiscriminantDisposition.HOLD
    assert "DIRECT_DIMENSION_ASSIGNMENT_MISMATCH" in result.reasons


def test_all_six_dimensions_cannot_be_force_bound_to_ccap() -> None:
    result = assess(
        specification(),
        candidate_dimensions=(D1, D2, D3, D4, D5, D6),
    )

    assert result.disposition is DimensionDiscriminantDisposition.HOLD
    assert "DIRECT_DIMENSION_ASSIGNMENT_MISMATCH" in result.reasons


def test_stale_frozen_dimension_source_digest_fails_closed() -> None:
    result = assess(specification(), current_source_sha256="0" * 64)

    assert result.disposition is DimensionDiscriminantDisposition.HOLD
    assert "FROZEN_DIMENSION_SOURCE_DIGEST_MISMATCH" in result.reasons


def test_system_boundary_content_drift_fails_closed() -> None:
    result = assess(specification(), current_boundary_sha256="0" * 64)

    assert result.disposition is DimensionDiscriminantDisposition.HOLD
    assert "SYSTEM_BOUNDARY_DIGEST_MISMATCH" in result.reasons


def test_system_boundary_must_be_fixed_before_dimension_assignment() -> None:
    value = specification(
        system_boundary=boundary(fixed_before_indicator_assignment=False)
    )
    result = assess(value)

    assert result.disposition is DimensionDiscriminantDisposition.HOLD
    assert "SYSTEM_BOUNDARY_NOT_FIXED_BEFORE_INDICATOR_ASSIGNMENT" in result.reasons


def test_every_direct_dimension_requires_near_neighbor_differential_prediction() -> None:
    only_d1 = (differential_predictions()[0],)
    result = assess(specification(predictions=only_d1))

    assert result.disposition is DimensionDiscriminantDisposition.HOLD
    assert (
        "DIRECT_DIMENSION_NEAR_NEIGHBOR_PREDICTION_MISSING:"
        "ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT"
    ) in result.reasons


def test_discriminant_prediction_cannot_use_its_target_as_its_own_neighbor() -> None:
    original = differential_predictions()[0]

    try:
        replace(original, near_neighbor_dimension=D1)
    except ValueError as exc:
        assert "distinct near-neighbor dimension" in str(exc)
    else:
        raise AssertionError("self-neighbor discriminant prediction must fail closed")
