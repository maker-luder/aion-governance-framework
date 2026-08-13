from __future__ import annotations

from dataclasses import replace

from aion_individuation_thresholds import (
    BoundaryPerturbation,
    CriterionKind,
    CriterionObservation,
    CriterionSpec,
    IndividuationProfile,
    ThresholdAuditStatus,
    ThresholdDirection,
    audit_individuation_profile,
)


REGISTRATION = "2026-01-01T00:00:00+00:00"
START = "2026-01-02T00:00:00+00:00"
END = "2026-01-03T00:00:00+00:00"


def criterion(criterion_id: str, threshold: float = 0.8) -> CriterionSpec:
    kind = (
        CriterionKind.TEMPORAL_INTEGRITY
        if criterion_id == "temporal"
        else CriterionKind.BOUNDARY_COHERENCE
    )
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
        "profile_id": "profile-test",
        "target_ref": "target:synthetic",
        "protocol_version": "individuation-protocol-v0.1.0",
        "registration_ref": "registration:synthetic",
        "registration_hash": "sha256:synthetic",
        "registration_timestamp": REGISTRATION,
        "observation_start": START,
        "observation_end": END,
        "criteria": (criterion("temporal"), criterion("boundary")),
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


def test_valid_profile_is_admissible_for_review_only() -> None:
    result = audit_individuation_profile(base_profile())
    assert result.status is ThresholdAuditStatus.ADMISSIBLE_FOR_REVIEW
    assert result.reason == "PROFILE_ADMISSIBLE_FOR_THRESHOLD_REVIEW_ONLY"
    assert all(item["cross_context_pass"] for item in result.criterion_results)


def test_valid_profile_reports_each_criterion_and_context_pass() -> None:
    payload = audit_individuation_profile(base_profile()).as_dict()
    assert payload["criterion_results"][0]["context_passes"] == [True, True]
    assert payload["criterion_results"][1]["context_passes"] == [True, True]
    assert payload["threshold_validated"] is False


def test_registration_must_precede_observation() -> None:
    result = audit_individuation_profile(
        base_profile(registration_timestamp="2026-01-02T00:00:00+00:00")
    )
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "REGISTRATION_NOT_BEFORE_OBSERVATION"


def test_thresholds_must_be_locked() -> None:
    result = audit_individuation_profile(base_profile(thresholds_locked=False))
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "THRESHOLDS_NOT_PREREGISTERED_OR_LOCKED"


def test_observation_window_must_be_ordered() -> None:
    result = audit_individuation_profile(
        base_profile(observation_start="2026-01-04T00:00:00+00:00")
    )
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "OBSERVATION_WINDOW_INVALID"


def test_missing_criterion_metadata_is_held() -> None:
    result = audit_individuation_profile(
        base_profile(criteria=(criterion("temporal"), replace(criterion("boundary"), measurement_ref="")))
    )
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "CRITERION_METADATA_INCOMPLETE"


def test_single_context_is_indeterminate() -> None:
    result = audit_individuation_profile(base_profile(required_context_count=1))
    assert result.status is ThresholdAuditStatus.INDETERMINATE
    assert result.reason == "CROSS_CONTEXT_VALIDATION_REQUIRES_AT_LEAST_TWO_CONTEXTS"


def test_incomplete_criterion_context_matrix_is_indeterminate() -> None:
    observations = tuple(base_profile().observations[:-1])
    result = audit_individuation_profile(base_profile(observations=observations))
    assert result.status is ThresholdAuditStatus.INDETERMINATE
    assert result.reason == "CRITERION_CONTEXT_MATRIX_INCOMPLETE"


def test_cross_context_instability_is_not_validation() -> None:
    observations = list(base_profile().observations)
    observations[-1] = observation("boundary", "ctx-b", 0.3)
    result = audit_individuation_profile(base_profile(observations=tuple(observations)))
    assert result.status is ThresholdAuditStatus.INDETERMINATE
    assert result.reason == "CROSS_CONTEXT_CRITERION_INSTABILITY"


def test_missing_boundary_perturbation_metadata_is_indeterminate() -> None:
    result = audit_individuation_profile(base_profile(perturbations=()))
    assert result.status is ThresholdAuditStatus.INDETERMINATE
    assert result.reason == "BOUNDARY_PERTURBATION_METADATA_MISSING"


def test_boundary_perturbation_execution_is_forbidden() -> None:
    perturbation = replace(base_profile().perturbations[0], observed=True)
    result = audit_individuation_profile(base_profile(perturbations=(perturbation,)))
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "BOUNDARY_PERTURBATION_EXECUTION_FORBIDDEN"


def test_contradiction_reference_requires_review() -> None:
    result = audit_individuation_profile(base_profile(contradiction_refs=("profile:other",)))
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "CONTRADICTORY_PROFILE_RECORDS_REQUIRE_REVIEW"
    assert result.contradiction_refs == ("profile:other",)


def test_identity_claim_cannot_be_established_by_threshold_contract() -> None:
    result = audit_individuation_profile(base_profile(identity_claim="IDENTITY_ESTABLISHED"))
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "INDIVIDUATION_CONTRACT_CANNOT_ESTABLISH_IDENTITY"


def test_duplicate_observations_are_held() -> None:
    observations = base_profile().observations + (observation("temporal", "ctx-a", 0.2),)
    result = audit_individuation_profile(base_profile(observations=observations))
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "DUPLICATE_OR_CONTRADICTORY_OBSERVATIONS_REQUIRE_REVIEW"


def test_invalid_threshold_domain_is_held() -> None:
    result = audit_individuation_profile(
        base_profile(criteria=(criterion("temporal", 1.2), criterion("boundary")))
    )
    assert result.status is ThresholdAuditStatus.HOLD
    assert result.reason == "CRITERION_THRESHOLD_OUT_OF_DOMAIN"


def test_all_decisions_preserve_non_promotion_invariants() -> None:
    candidates = (
        base_profile(),
        base_profile(thresholds_locked=False),
        base_profile(identity_claim="IDENTITY_ESTABLISHED"),
        base_profile(contradiction_refs=("profile:other",)),
    )
    for candidate in candidates:
        payload = audit_individuation_profile(candidate).as_dict()
        assert payload["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert payload["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
        assert payload["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert payload["canonical_effect"] == "NONE"
        assert payload["governance_effect"] == "NONE"
        assert payload["deployment"] is False
