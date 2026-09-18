from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .evidence_dimensions import SubjectivityEvidenceDimension


_HEX = set("0123456789abcdef")


class DimensionDiscriminantDisposition(StrEnum):
    READY_FOR_ADVERSARIAL_REVIEW = "READY_FOR_ADVERSARIAL_REVIEW"
    HOLD = "HOLD"


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_sha256(name: str, value: str) -> None:
    if len(value) != 64 or any(char not in _HEX for char in value.lower()):
        raise ValueError(f"{name} must be a 64-character hexadecimal SHA-256")


@dataclass(frozen=True, slots=True)
class SystemBoundarySpecification:
    boundary_id: str
    subject_ref: str
    boundary_ref: str
    boundary_sha256: str
    included_loci: tuple[str, ...]
    excluded_loci: tuple[str, ...]
    fixed_before_indicator_assignment: bool

    def __post_init__(self) -> None:
        for name in ("boundary_id", "subject_ref", "boundary_ref"):
            _require_text(name, getattr(self, name))
        _require_sha256("boundary_sha256", self.boundary_sha256)
        if not self.included_loci:
            raise ValueError("included_loci must be non-empty")
        if any(not item.strip() for item in (*self.included_loci, *self.excluded_loci)):
            raise ValueError("system-boundary loci must be non-empty")
        if set(self.included_loci) & set(self.excluded_loci):
            raise ValueError("system-boundary included and excluded loci must not overlap")


@dataclass(frozen=True, slots=True)
class DimensionDifferentialPrediction:
    prediction_id: str
    target_dimension: SubjectivityEvidenceDimension
    near_neighbor_dimension: SubjectivityEvidenceDimension
    perturbation_ref: str
    target_prediction: str
    near_neighbor_prediction: str
    falsifier: str

    def __post_init__(self) -> None:
        for name in (
            "prediction_id",
            "perturbation_ref",
            "target_prediction",
            "near_neighbor_prediction",
            "falsifier",
        ):
            _require_text(name, getattr(self, name))
        if self.target_dimension is self.near_neighbor_dimension:
            raise ValueError("a discriminant prediction requires a distinct near-neighbor dimension")


@dataclass(frozen=True, slots=True)
class DimensionBindingSpecification:
    specification_id: str
    source_ref: str
    source_sha256: str
    direct_dimensions: tuple[SubjectivityEvidenceDimension, ...]
    conditional_dimensions: tuple[SubjectivityEvidenceDimension, ...]
    closed_dimensions: tuple[SubjectivityEvidenceDimension, ...]
    system_boundary: SystemBoundarySpecification
    differential_predictions: tuple[DimensionDifferentialPrediction, ...]
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        _require_text("specification_id", self.specification_id)
        _require_text("source_ref", self.source_ref)
        _require_sha256("source_sha256", self.source_sha256)

        groups = (
            self.direct_dimensions,
            self.conditional_dimensions,
            self.closed_dimensions,
        )
        flattened = tuple(item for group in groups for item in group)
        if len(flattened) != len(set(flattened)):
            raise ValueError("dimension coverage groups must be mutually exclusive")
        if set(flattened) != set(SubjectivityEvidenceDimension):
            raise ValueError("dimension coverage groups must partition all six standing dimensions")
        if not self.direct_dimensions:
            raise ValueError("at least one direct dimension is required for a discriminant audit")

        prediction_ids = tuple(item.prediction_id for item in self.differential_predictions)
        if len(prediction_ids) != len(set(prediction_ids)):
            raise ValueError("differential prediction identifiers must be unique")

        if self.scientific_disposition != "HOLD":
            raise ValueError("dimension-binding scientific disposition must remain HOLD")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("dimension binding cannot establish subjectivity")
        if self.canonical_effect != "NONE":
            raise ValueError("dimension-binding specification cannot create canonical effect")


@dataclass(frozen=True, slots=True)
class DimensionDiscriminantAssessment:
    specification_id: str
    disposition: DimensionDiscriminantDisposition
    reasons: tuple[str, ...]
    independent_validation_status: str = "NOT_ACHIEVED"
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"


class DimensionDiscriminantAudit:
    """Fail-closed pre-execution audit for dimension mapping discriminability.

    The audit verifies frozen-source identity, system-boundary ordering, exact direct
    dimension assignment and ex-ante near-neighbor differential predictions. It does
    not decide whether those predictions are scientifically correct and does not
    provide independent validation.
    """

    def assess(
        self,
        specification: DimensionBindingSpecification,
        *,
        candidate_dimensions: tuple[SubjectivityEvidenceDimension, ...],
        current_source_sha256: str,
        current_boundary_sha256: str,
    ) -> DimensionDiscriminantAssessment:
        _require_sha256("current_source_sha256", current_source_sha256)
        _require_sha256("current_boundary_sha256", current_boundary_sha256)

        reasons: list[str] = ["DIMENSION_DISCRIMINANT_AUDIT_EVALUATED"]

        if current_source_sha256 != specification.source_sha256:
            reasons.append("FROZEN_DIMENSION_SOURCE_DIGEST_MISMATCH")
        if current_boundary_sha256 != specification.system_boundary.boundary_sha256:
            reasons.append("SYSTEM_BOUNDARY_DIGEST_MISMATCH")
        if not specification.system_boundary.fixed_before_indicator_assignment:
            reasons.append("SYSTEM_BOUNDARY_NOT_FIXED_BEFORE_INDICATOR_ASSIGNMENT")

        if len(candidate_dimensions) != len(set(candidate_dimensions)):
            reasons.append("DUPLICATE_CANDIDATE_DIMENSION_BINDING")
        if set(candidate_dimensions) != set(specification.direct_dimensions):
            reasons.append("DIRECT_DIMENSION_ASSIGNMENT_MISMATCH")

        predictions_by_target = {
            dimension: [
                prediction
                for prediction in specification.differential_predictions
                if prediction.target_dimension is dimension
            ]
            for dimension in specification.direct_dimensions
        }
        missing = [
            dimension.value
            for dimension, predictions in predictions_by_target.items()
            if not predictions
        ]
        if missing:
            reasons.append(
                "DIRECT_DIMENSION_NEAR_NEIGHBOR_PREDICTION_MISSING:" + ",".join(sorted(missing))
            )

        if any(
            prediction.near_neighbor_dimension is prediction.target_dimension
            for prediction in specification.differential_predictions
        ):
            reasons.append("INVALID_SELF_NEIGHBOR_DISCRIMINANT_PREDICTION")

        if any(
            reason.startswith(
                (
                    "FROZEN_",
                    "SYSTEM_",
                    "DUPLICATE_",
                    "DIRECT_",
                    "INVALID_",
                )
            )
            for reason in reasons
        ):
            return DimensionDiscriminantAssessment(
                specification_id=specification.specification_id,
                disposition=DimensionDiscriminantDisposition.HOLD,
                reasons=tuple(reasons),
            )

        reasons.extend(
            (
                "FROZEN_SOURCE_CONTENT_BOUND",
                "SYSTEM_BOUNDARY_FIXED_BEFORE_INDICATOR_ASSIGNMENT",
                "DIRECT_DIMENSION_ASSIGNMENT_MATCHES_FROZEN_SPECIFICATION",
                "NEAR_NEIGHBOR_DIFFERENTIAL_PREDICTIONS_PRESENT",
                "STRUCTURAL_DISCRIMINANT_READINESS_IS_NOT_EMPIRICAL_VALIDATION",
                "INDEPENDENT_VALIDATION_NOT_ACHIEVED",
            )
        )
        return DimensionDiscriminantAssessment(
            specification_id=specification.specification_id,
            disposition=DimensionDiscriminantDisposition.READY_FOR_ADVERSARIAL_REVIEW,
            reasons=tuple(reasons),
        )
