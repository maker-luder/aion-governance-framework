from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum


class SubjectivityEvidenceDimension(str, Enum):
    CAUSAL_BOUNDARY = "CAUSAL_BOUNDARY"
    DIACHRONIC_CONTINUITY = "DIACHRONIC_CONTINUITY"
    SELF_MODEL_CAUSAL_ROLE = "SELF_MODEL_CAUSAL_ROLE"
    ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT = "ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT"
    COUNTERFACTUAL_SELF_CONSISTENCY = "COUNTERFACTUAL_SELF_CONSISTENCY"
    SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE = "SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE"


class EvidenceDisposition(str, Enum):
    SUPPORTS_ORGANIZATION_HYPOTHESIS = "SUPPORTS_ORGANIZATION_HYPOTHESIS"
    SUPPORTS_ALTERNATIVE_EXPLANATION = "SUPPORTS_ALTERNATIVE_EXPLANATION"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_TESTED = "NOT_TESTED"


class IndicatorPolarity(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class TheoryFamily(str, Enum):
    RECURRENT_PROCESSING = "RECURRENT_PROCESSING"
    GLOBAL_WORKSPACE = "GLOBAL_WORKSPACE"
    HIGHER_ORDER = "HIGHER_ORDER"
    PREDICTIVE_PROCESSING = "PREDICTIVE_PROCESSING"
    ATTENTION_SCHEMA = "ATTENTION_SCHEMA"
    AGENCY_EMBODIMENT = "AGENCY_EMBODIMENT"
    THEORY_NEUTRAL = "THEORY_NEUTRAL"


class TheoryTestMode(str, Enum):
    EXPLORATORY = "EXPLORATORY"
    PREREGISTERED_ADVERSARIAL = "PREREGISTERED_ADVERSARIAL"


_CAUSAL_SUPPORT_DIMENSIONS = {
    SubjectivityEvidenceDimension.CAUSAL_BOUNDARY,
    SubjectivityEvidenceDimension.SELF_MODEL_CAUSAL_ROLE,
    SubjectivityEvidenceDimension.ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT,
    SubjectivityEvidenceDimension.SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE,
}


@dataclass(frozen=True, slots=True)
class TheoryIndicatorRecord:
    indicator_id: str
    theory_family: TheoryFamily
    computational_property: str
    polarity: IndicatorPolarity
    source_ref: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.indicator_id.strip() or not self.computational_property.strip():
            raise ValueError("theory indicator id and computational property are required")
        if not self.source_ref.strip():
            raise ValueError("theory indicator source_ref is required")
        if any(not item.strip() for item in self.evidence_refs):
            raise ValueError("theory indicator evidence refs must be non-empty")


@dataclass(frozen=True, slots=True)
class DimensionObservation:
    dimension: SubjectivityEvidenceDimension
    disposition: EvidenceDisposition
    mechanism_ref: str
    evidence_refs: tuple[str, ...]
    competing_explanations: tuple[str, ...]
    indicator_refs: tuple[str, ...] = field(default_factory=tuple)
    intervention_sensitive: bool = False
    self_report_only: bool = False

    def __post_init__(self) -> None:
        if not self.mechanism_ref.strip():
            raise ValueError("dimension observation mechanism_ref is required")
        if any(not item.strip() for item in self.evidence_refs):
            raise ValueError("dimension observation evidence refs must be non-empty")
        if any(not item.strip() for item in self.competing_explanations):
            raise ValueError("competing explanations must be non-empty")
        if any(not item.strip() for item in self.indicator_refs):
            raise ValueError("indicator refs must be non-empty")
        if self.disposition is not EvidenceDisposition.NOT_TESTED and not self.evidence_refs:
            raise ValueError("tested dimensions require evidence refs")
        if self.disposition is EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS:
            if not self.competing_explanations:
                raise ValueError("supporting evidence requires explicit competing explanations")
            if self.self_report_only:
                raise ValueError("SELF_REPORT_ONLY != SUBJECTIVITY_SUPPORT")
            if self.dimension in _CAUSAL_SUPPORT_DIMENSIONS and not self.intervention_sensitive:
                raise ValueError("causal-role support requires intervention-sensitive evidence")


@dataclass(frozen=True, slots=True)
class SubjectivityEvidenceMatrix:
    subject_ref: str
    protocol_ref: str
    observations: tuple[DimensionObservation, ...]
    indicators: tuple[TheoryIndicatorRecord, ...] = field(default_factory=tuple)
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.subject_ref.strip() or not self.protocol_ref.strip():
            raise ValueError("subject_ref and protocol_ref are required")
        dimensions = tuple(item.dimension for item in self.observations)
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("subjectivity evidence dimensions must be unique")
        if set(dimensions) != set(SubjectivityEvidenceDimension):
            raise ValueError("subjectivity evidence matrix requires exactly the six standing dimensions")

        indicator_ids = tuple(item.indicator_id for item in self.indicators)
        if len(indicator_ids) != len(set(indicator_ids)):
            raise ValueError("theory indicator identifiers must be unique")
        known = set(indicator_ids)
        unknown_refs = {
            indicator_ref
            for observation in self.observations
            for indicator_ref in observation.indicator_refs
            if indicator_ref not in known
        }
        if unknown_refs:
            raise ValueError(f"unknown theory indicator refs: {sorted(unknown_refs)}")

        if self.scientific_disposition != "HOLD":
            raise ValueError("subjectivity evidence matrix scientific disposition must remain HOLD")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("SUBJECTIVITY_EVIDENCE != SUBJECTIVITY")
        if self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise ValueError("MECHANISM_EVIDENCE != PHENOMENAL_EXPERIENCE")
        if self.canonical_effect != "NONE":
            raise ValueError("research evidence matrix must keep canonical_effect=NONE")

    @property
    def supporting_dimensions(self) -> tuple[SubjectivityEvidenceDimension, ...]:
        return tuple(
            item.dimension
            for item in self.observations
            if item.disposition is EvidenceDisposition.SUPPORTS_ORGANIZATION_HYPOTHESIS
        )

    @property
    def counterevidence_dimensions(self) -> tuple[SubjectivityEvidenceDimension, ...]:
        return tuple(
            item.dimension
            for item in self.observations
            if item.disposition is EvidenceDisposition.SUPPORTS_ALTERNATIVE_EXPLANATION
        )

    @property
    def unresolved_dimensions(self) -> tuple[SubjectivityEvidenceDimension, ...]:
        return tuple(
            item.dimension
            for item in self.observations
            if item.disposition in {EvidenceDisposition.INCONCLUSIVE, EvidenceDisposition.NOT_TESTED}
        )

    @property
    def fingerprint(self) -> str:
        payload = {
            "subject_ref": self.subject_ref,
            "protocol_ref": self.protocol_ref,
            "observations": [
                {
                    "dimension": item.dimension.value,
                    "disposition": item.disposition.value,
                    "mechanism_ref": item.mechanism_ref,
                    "evidence_refs": item.evidence_refs,
                    "competing_explanations": item.competing_explanations,
                    "indicator_refs": item.indicator_refs,
                    "intervention_sensitive": item.intervention_sensitive,
                    "self_report_only": item.self_report_only,
                }
                for item in self.observations
            ],
            "indicators": [
                {
                    "indicator_id": item.indicator_id,
                    "theory_family": item.theory_family.value,
                    "computational_property": item.computational_property,
                    "polarity": item.polarity.value,
                    "source_ref": item.source_ref,
                    "evidence_refs": item.evidence_refs,
                }
                for item in self.indicators
            ],
            "scientific_disposition": self.scientific_disposition,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "phenomenal_experience_conclusion": self.phenomenal_experience_conclusion,
            "canonical_effect": self.canonical_effect,
        }
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class AdversarialPrediction:
    theory_family: TheoryFamily
    prediction: str
    falsifier: str
    interpretation_if_supported: str
    interpretation_if_failed: str

    def __post_init__(self) -> None:
        if self.theory_family is TheoryFamily.THEORY_NEUTRAL:
            raise ValueError("adversarial predictions must belong to a substantive theory family")
        for field_name in (
            "prediction",
            "falsifier",
            "interpretation_if_supported",
            "interpretation_if_failed",
        ):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")


@dataclass(frozen=True, slots=True)
class AdversarialTheoryTest:
    test_id: str
    mode: TheoryTestMode
    predictions: tuple[AdversarialPrediction, ...]
    preregistration_ref: str | None = None
    held_out_evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    posthoc_prediction_rewrite: bool = False
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.test_id.strip():
            raise ValueError("adversarial test_id is required")
        theories = {item.theory_family for item in self.predictions}
        if len(theories) < 2:
            raise ValueError("adversarial theory testing requires at least two competing theory families")
        if self.preregistration_ref is not None and not self.preregistration_ref.strip():
            raise ValueError("preregistration_ref must be non-empty when provided")
        if any(not item.strip() for item in self.held_out_evidence_refs):
            raise ValueError("held-out evidence refs must be non-empty")
        if self.mode is TheoryTestMode.PREREGISTERED_ADVERSARIAL:
            if self.preregistration_ref is None or not self.held_out_evidence_refs:
                raise ValueError(
                    "preregistered adversarial testing requires a preregistration ref and held-out evidence refs"
                )
            if self.posthoc_prediction_rewrite:
                raise ValueError("post-hoc prediction rewriting invalidates preregistered adversarial testing")
        if self.scientific_disposition != "HOLD":
            raise ValueError("theory-test scientific disposition must remain HOLD")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("THEORY_SUPPORT != SUBJECTIVITY_PROOF")
        if self.canonical_effect != "NONE":
            raise ValueError("adversarial research test must keep canonical_effect=NONE")

    @property
    def fingerprint(self) -> str:
        payload = {
            "test_id": self.test_id,
            "mode": self.mode.value,
            "predictions": [
                {
                    "theory_family": item.theory_family.value,
                    "prediction": item.prediction,
                    "falsifier": item.falsifier,
                    "interpretation_if_supported": item.interpretation_if_supported,
                    "interpretation_if_failed": item.interpretation_if_failed,
                }
                for item in self.predictions
            ],
            "preregistration_ref": self.preregistration_ref,
            "held_out_evidence_refs": self.held_out_evidence_refs,
            "posthoc_prediction_rewrite": self.posthoc_prediction_rewrite,
            "scientific_disposition": self.scientific_disposition,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "canonical_effect": self.canonical_effect,
        }
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
