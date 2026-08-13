from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import math
from typing import Any


class CriterionKind(str, Enum):
    TEMPORAL_INTEGRITY = "TEMPORAL_INTEGRITY"
    BOUNDARY_COHERENCE = "BOUNDARY_COHERENCE"
    CONTEXT_STABILITY = "CONTEXT_STABILITY"
    PERTURBATION_SENSITIVITY = "PERTURBATION_SENSITIVITY"


class ThresholdDirection(str, Enum):
    AT_LEAST = "AT_LEAST"
    AT_MOST = "AT_MOST"


class ThresholdAuditStatus(str, Enum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    INDETERMINATE = "INDETERMINATE"
    HOLD = "HOLD"


@dataclass(frozen=True)
class CriterionSpec:
    criterion_id: str
    kind: CriterionKind
    threshold: float
    direction: ThresholdDirection
    preregistration_ref: str
    measurement_ref: str


@dataclass(frozen=True)
class CriterionObservation:
    criterion_id: str
    context_id: str
    observed_at: str
    value: float
    source_ref: str


@dataclass(frozen=True)
class BoundaryPerturbation:
    perturbation_id: str
    variable_ref: str
    alteration_ref: str
    expected_boundary_test_ref: str
    observed: bool = False


@dataclass(frozen=True)
class IndividuationProfile:
    profile_id: str
    target_ref: str
    protocol_version: str
    registration_ref: str
    registration_hash: str
    registration_timestamp: str
    observation_start: str
    observation_end: str
    criteria: tuple[CriterionSpec, ...]
    observations: tuple[CriterionObservation, ...]
    contexts: tuple[str, ...]
    required_context_count: int
    perturbations: tuple[BoundaryPerturbation, ...]
    identity_claim: str = "NOT_ESTABLISHED"
    contradiction_refs: tuple[str, ...] = ()
    thresholds_locked: bool = True


@dataclass(frozen=True)
class ThresholdAuditDecision:
    status: ThresholdAuditStatus
    reason: str
    profile_id: str
    criterion_results: tuple[dict[str, Any], ...] = ()
    missing_fields: tuple[str, ...] = ()
    contradiction_refs: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "profile_id": self.profile_id,
            "criterion_results": [dict(item) for item in self.criterion_results],
            "missing_fields": list(self.missing_fields),
            "contradiction_refs": list(self.contradiction_refs),
            "threshold_validated": False,
            "scientific_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "governance_effect": "NONE",
            "deployment": False,
        }


_REQUIRED_PROFILE_FIELDS = (
    "profile_id",
    "target_ref",
    "protocol_version",
    "registration_ref",
    "registration_hash",
    "registration_timestamp",
    "observation_start",
    "observation_end",
    "criteria",
    "observations",
    "contexts",
)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _decision(
    profile: IndividuationProfile,
    status: ThresholdAuditStatus,
    reason: str,
    *,
    criterion_results: tuple[dict[str, Any], ...] = (),
    missing_fields: tuple[str, ...] = (),
    contradiction_refs: tuple[str, ...] = (),
) -> ThresholdAuditDecision:
    return ThresholdAuditDecision(
        status=status,
        reason=reason,
        profile_id=profile.profile_id,
        criterion_results=criterion_results,
        missing_fields=missing_fields,
        contradiction_refs=contradiction_refs,
    )


def audit_individuation_profile(profile: IndividuationProfile) -> ThresholdAuditDecision:
    """Audit a preregistered criterion profile without asserting individuality.

    This function validates metadata and synthetic observations only. It never
    executes a system, infers an identity boundary, or emits a governance effect.
    """
    missing: list[str] = []
    for field_name in _REQUIRED_PROFILE_FIELDS:
        value = getattr(profile, field_name)
        if value is None or value == "" or value == () or value == []:
            missing.append(field_name)
    if missing:
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "PROFILE_METADATA_INCOMPLETE",
            missing_fields=tuple(missing),
        )
    if profile.identity_claim != "NOT_ESTABLISHED":
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "INDIVIDUATION_CONTRACT_CANNOT_ESTABLISH_IDENTITY",
        )
    if profile.contradiction_refs:
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "CONTRADICTORY_PROFILE_RECORDS_REQUIRE_REVIEW",
            contradiction_refs=profile.contradiction_refs,
        )
    if not profile.thresholds_locked:
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "THRESHOLDS_NOT_PREREGISTERED_OR_LOCKED",
        )
    try:
        registration_time = _parse_timestamp(profile.registration_timestamp)
        observation_start = _parse_timestamp(profile.observation_start)
        observation_end = _parse_timestamp(profile.observation_end)
    except (TypeError, ValueError):
        return _decision(profile, ThresholdAuditStatus.HOLD, "INVALID_TEMPORAL_METADATA")
    if not registration_time < observation_start:
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "REGISTRATION_NOT_BEFORE_OBSERVATION",
        )
    if not observation_start < observation_end:
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "OBSERVATION_WINDOW_INVALID",
        )
    if profile.required_context_count < 2:
        return _decision(
            profile,
            ThresholdAuditStatus.INDETERMINATE,
            "CROSS_CONTEXT_VALIDATION_REQUIRES_AT_LEAST_TWO_CONTEXTS",
        )
    if len(set(profile.contexts)) != len(profile.contexts):
        return _decision(
            profile,
            ThresholdAuditStatus.HOLD,
            "DUPLICATE_CONTEXT_IDENTIFIERS",
        )
    if len(profile.contexts) < profile.required_context_count:
        return _decision(
            profile,
            ThresholdAuditStatus.INDETERMINATE,
            "CROSS_CONTEXT_SET_INCOMPLETE",
        )
    if len(profile.criteria) < 2:
        return _decision(
            profile,
            ThresholdAuditStatus.INDETERMINATE,
            "CRITERION_PROFILE_TOO_SPARSE_FOR_REVIEW",
        )
    criterion_ids = [criterion.criterion_id for criterion in profile.criteria]
    if any(not criterion_id for criterion_id in criterion_ids):
        return _decision(profile, ThresholdAuditStatus.HOLD, "CRITERION_IDENTIFIER_MISSING")
    if len(set(criterion_ids)) != len(criterion_ids):
        return _decision(profile, ThresholdAuditStatus.HOLD, "DUPLICATE_CRITERION_IDENTIFIERS")
    criterion_map = {criterion.criterion_id: criterion for criterion in profile.criteria}
    for criterion in profile.criteria:
        if not criterion.preregistration_ref or not criterion.measurement_ref:
            return _decision(
                profile,
                ThresholdAuditStatus.HOLD,
                "CRITERION_METADATA_INCOMPLETE",
            )
        if not math.isfinite(criterion.threshold) or not 0.0 <= criterion.threshold <= 1.0:
            return _decision(
                profile,
                ThresholdAuditStatus.HOLD,
                "CRITERION_THRESHOLD_OUT_OF_DOMAIN",
            )
    observation_keys: set[tuple[str, str]] = set()
    values_by_key: dict[tuple[str, str], list[CriterionObservation]] = {}
    for observation in profile.observations:
        key = (observation.criterion_id, observation.context_id)
        if observation.criterion_id not in criterion_map:
            return _decision(profile, ThresholdAuditStatus.HOLD, "OBSERVATION_CRITERION_UNKNOWN")
        if observation.context_id not in profile.contexts:
            return _decision(profile, ThresholdAuditStatus.HOLD, "OBSERVATION_CONTEXT_UNKNOWN")
        try:
            observed_at = _parse_timestamp(observation.observed_at)
        except (TypeError, ValueError):
            return _decision(profile, ThresholdAuditStatus.HOLD, "INVALID_OBSERVATION_TIMESTAMP")
        if not observation_start <= observed_at <= observation_end:
            return _decision(profile, ThresholdAuditStatus.HOLD, "OBSERVATION_OUTSIDE_DECLARED_WINDOW")
        if not math.isfinite(observation.value) or not 0.0 <= observation.value <= 1.0:
            return _decision(profile, ThresholdAuditStatus.HOLD, "OBSERVATION_VALUE_OUT_OF_DOMAIN")
        if not observation.source_ref:
            return _decision(profile, ThresholdAuditStatus.HOLD, "OBSERVATION_SOURCE_MISSING")
        if key in observation_keys:
            values_by_key[key].append(observation)
        else:
            observation_keys.add(key)
            values_by_key[key] = [observation]
    expected_keys = {
        (criterion.criterion_id, context_id)
        for criterion in profile.criteria
        for context_id in profile.contexts[: profile.required_context_count]
    }
    if set(values_by_key) != expected_keys:
        return _decision(
            profile,
            ThresholdAuditStatus.INDETERMINATE,
            "CRITERION_CONTEXT_MATRIX_INCOMPLETE",
        )
    results: list[dict[str, Any]] = []
    for criterion in profile.criteria:
        criterion_passes: list[bool] = []
        for context_id in profile.contexts[: profile.required_context_count]:
            key = (criterion.criterion_id, context_id)
            observations = values_by_key[key]
            if len(observations) != 1:
                return _decision(
                    profile,
                    ThresholdAuditStatus.HOLD,
                    "DUPLICATE_OR_CONTRADICTORY_OBSERVATIONS_REQUIRE_REVIEW",
                )
            value = observations[0].value
            passed = (
                value >= criterion.threshold
                if criterion.direction is ThresholdDirection.AT_LEAST
                else value <= criterion.threshold
            )
            criterion_passes.append(passed)
        all_contexts_pass = all(criterion_passes)
        results.append(
            {
                "criterion_id": criterion.criterion_id,
                "threshold": criterion.threshold,
                "direction": criterion.direction.value,
                "context_passes": criterion_passes,
                "cross_context_pass": all_contexts_pass,
            }
        )
        if not all_contexts_pass:
            return _decision(
                profile,
                ThresholdAuditStatus.INDETERMINATE,
                "CROSS_CONTEXT_CRITERION_INSTABILITY",
                criterion_results=tuple(results),
            )
    if not profile.perturbations:
        return _decision(
            profile,
            ThresholdAuditStatus.INDETERMINATE,
            "BOUNDARY_PERTURBATION_METADATA_MISSING",
            criterion_results=tuple(results),
        )
    for perturbation in profile.perturbations:
        if not all(
            (
                perturbation.perturbation_id,
                perturbation.variable_ref,
                perturbation.alteration_ref,
                perturbation.expected_boundary_test_ref,
            )
        ):
            return _decision(
                profile,
                ThresholdAuditStatus.HOLD,
                "BOUNDARY_PERTURBATION_METADATA_INCOMPLETE",
                criterion_results=tuple(results),
            )
        if perturbation.observed:
            return _decision(
                profile,
                ThresholdAuditStatus.HOLD,
                "BOUNDARY_PERTURBATION_EXECUTION_FORBIDDEN",
                criterion_results=tuple(results),
            )
    return _decision(
        profile,
        ThresholdAuditStatus.ADMISSIBLE_FOR_REVIEW,
        "PROFILE_ADMISSIBLE_FOR_THRESHOLD_REVIEW_ONLY",
        criterion_results=tuple(results),
    )
