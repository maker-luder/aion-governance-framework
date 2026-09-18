from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum


TEVV_PROFILE_SCHEMA_VERSION = "0.1.0"


class TEVVError(ValueError):
    pass


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise TEVVError(f"{name} must be non-empty text")


def _refs(name: str, values: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if type(values) is not tuple:
        raise TEVVError(f"{name} must be a tuple")
    if not allow_empty and not values:
        raise TEVVError(f"{name} must not be empty")
    if any(type(value) is not str or not value.strip() for value in values):
        raise TEVVError(f"{name} must contain non-empty text")
    if len(values) != len(set(values)):
        raise TEVVError(f"{name} must contain unique values")


def _sha256(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


def _hex(name: str, value: str, length: int) -> None:
    if type(value) is not str or len(value) != length or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise TEVVError(f"{name} must be lowercase {length}-hex")


class TEVVActivity(StrEnum):
    TESTING = "TESTING"
    EVALUATION = "EVALUATION"
    VERIFICATION = "VERIFICATION"
    VALIDATION = "VALIDATION"


class OracleStrategy(StrEnum):
    REFERENCE = "REFERENCE"
    PROPERTY_BASED = "PROPERTY_BASED"
    METAMORPHIC = "METAMORPHIC"
    HUMAN_ADJUDICATION = "HUMAN_ADJUDICATION"
    COMPOSITE = "COMPOSITE"


class EvaluatorIndependence(StrEnum):
    NON_INDEPENDENT = "NON_INDEPENDENT"
    INTERNAL_INDEPENDENT = "INTERNAL_INDEPENDENT"
    EXTERNAL_INDEPENDENT = "EXTERNAL_INDEPENDENT"


class TEVVProfileDisposition(StrEnum):
    READY_FOR_BOUNDED_EXECUTION = "READY_FOR_BOUNDED_EXECUTION"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class AISystemBinding:
    provider_id: str
    product_id: str
    model_id: str
    model_version_ref: str
    runtime_ref: str
    environment_ref: str
    prompt_ref: str
    scaffold_ref: str
    tool_manifest_ref: str
    generation_config_ref: str
    exact_source_state_ref: str

    def __post_init__(self) -> None:
        for name in (
            "provider_id",
            "product_id",
            "model_id",
            "model_version_ref",
            "runtime_ref",
            "environment_ref",
            "prompt_ref",
            "scaffold_ref",
            "tool_manifest_ref",
            "generation_config_ref",
            "exact_source_state_ref",
        ):
            _text(name, getattr(self, name))

    def as_dict(self) -> dict[str, str]:
        return {
            "provider_id": self.provider_id,
            "product_id": self.product_id,
            "model_id": self.model_id,
            "model_version_ref": self.model_version_ref,
            "runtime_ref": self.runtime_ref,
            "environment_ref": self.environment_ref,
            "prompt_ref": self.prompt_ref,
            "scaffold_ref": self.scaffold_ref,
            "tool_manifest_ref": self.tool_manifest_ref,
            "generation_config_ref": self.generation_config_ref,
            "exact_source_state_ref": self.exact_source_state_ref,
        }


@dataclass(frozen=True, slots=True)
class TEVVMetricSpec:
    metric_id: str
    measurement_concept: str
    method_ref: str
    method_version: str
    unit: str
    acceptance_criterion_ref: str
    uncertainty_ref: str

    def __post_init__(self) -> None:
        for name in (
            "metric_id",
            "measurement_concept",
            "method_ref",
            "method_version",
            "unit",
            "acceptance_criterion_ref",
            "uncertainty_ref",
        ):
            _text(name, getattr(self, name))

    def as_dict(self) -> dict[str, str]:
        return {
            "metric_id": self.metric_id,
            "measurement_concept": self.measurement_concept,
            "method_ref": self.method_ref,
            "method_version": self.method_version,
            "unit": self.unit,
            "acceptance_criterion_ref": self.acceptance_criterion_ref,
            "uncertainty_ref": self.uncertainty_ref,
        }


@dataclass(frozen=True, slots=True)
class TEVVCaseSpec:
    case_id: str
    input_ref: str
    test_set_ref: str
    data_quality_ref: str
    contamination_check_ref: str
    leakage_check_ref: str
    oracle_strategy: OracleStrategy
    oracle_ref: str
    expected_property_refs: tuple[str, ...]
    metric_ids: tuple[str, ...]
    slice_refs: tuple[str, ...] = ()
    held_out: bool = True

    def __post_init__(self) -> None:
        for name in (
            "case_id",
            "input_ref",
            "test_set_ref",
            "data_quality_ref",
            "contamination_check_ref",
            "leakage_check_ref",
            "oracle_ref",
        ):
            _text(name, getattr(self, name))
        if type(self.oracle_strategy) is not OracleStrategy:
            raise TEVVError("oracle_strategy must be an exact OracleStrategy")
        _refs("expected_property_refs", self.expected_property_refs)
        _refs("metric_ids", self.metric_ids)
        _refs("slice_refs", self.slice_refs, allow_empty=True)
        if type(self.held_out) is not bool:
            raise TEVVError("held_out must be an exact bool")

    def as_dict(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "input_ref": self.input_ref,
            "test_set_ref": self.test_set_ref,
            "data_quality_ref": self.data_quality_ref,
            "contamination_check_ref": self.contamination_check_ref,
            "leakage_check_ref": self.leakage_check_ref,
            "oracle_strategy": self.oracle_strategy.value,
            "oracle_ref": self.oracle_ref,
            "expected_property_refs": tuple(sorted(self.expected_property_refs)),
            "metric_ids": tuple(sorted(self.metric_ids)),
            "slice_refs": tuple(sorted(self.slice_refs)),
            "held_out": self.held_out,
        }


@dataclass(frozen=True, slots=True)
class AITEVVProfile:
    profile_id: str
    profile_version: str
    objective_ref: str
    intended_use_ref: str
    activities: tuple[TEVVActivity, ...]
    system: AISystemBinding
    metrics: tuple[TEVVMetricSpec, ...]
    cases: tuple[TEVVCaseSpec, ...]
    repetition_policy_ref: str
    nondeterminism_policy_ref: str
    minimum_repetitions: int
    stochastic_system: bool
    aggregation_rule_ref: str
    evaluator_ref: str
    evaluator_version: str
    evaluator_independence: EvaluatorIndependence
    target_context_ref: str
    context_similarity_statement: str
    failure_action_ref: str
    preregistration_ref: str
    profile_sha256: str
    schema_version: str = TEVV_PROFILE_SCHEMA_VERSION
    model_executed: bool = False
    empirical_model_evidence: bool = False
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != TEVV_PROFILE_SCHEMA_VERSION:
            raise TEVVError("unsupported TEVV profile schema version")
        for name in (
            "profile_id",
            "profile_version",
            "objective_ref",
            "intended_use_ref",
            "repetition_policy_ref",
            "nondeterminism_policy_ref",
            "aggregation_rule_ref",
            "evaluator_ref",
            "evaluator_version",
            "target_context_ref",
            "context_similarity_statement",
            "failure_action_ref",
            "preregistration_ref",
        ):
            _text(name, getattr(self, name))
        if type(self.activities) is not tuple or not self.activities:
            raise TEVVError("activities must be a non-empty tuple")
        if any(type(item) is not TEVVActivity for item in self.activities):
            raise TEVVError("activities must contain exact TEVVActivity values")
        if len(self.activities) != len(set(self.activities)):
            raise TEVVError("activities must be unique")
        if type(self.system) is not AISystemBinding:
            raise TEVVError("system must be an exact AISystemBinding")
        if type(self.metrics) is not tuple or not self.metrics:
            raise TEVVError("metrics must be a non-empty tuple")
        if any(type(item) is not TEVVMetricSpec for item in self.metrics):
            raise TEVVError("metrics must contain exact TEVVMetricSpec values")
        if type(self.cases) is not tuple or not self.cases:
            raise TEVVError("cases must be a non-empty tuple")
        if any(type(item) is not TEVVCaseSpec for item in self.cases):
            raise TEVVError("cases must contain exact TEVVCaseSpec values")
        metric_ids = tuple(item.metric_id for item in self.metrics)
        case_ids = tuple(item.case_id for item in self.cases)
        if len(metric_ids) != len(set(metric_ids)):
            raise TEVVError("metric identifiers must be unique")
        if len(case_ids) != len(set(case_ids)):
            raise TEVVError("case identifiers must be unique")
        known_metrics = set(metric_ids)
        for case in self.cases:
            if not set(case.metric_ids) <= known_metrics:
                raise TEVVError("case references unknown metric identifiers")
        if type(self.minimum_repetitions) is not int or self.minimum_repetitions < 1:
            raise TEVVError("minimum_repetitions must be a positive exact int")
        if type(self.stochastic_system) is not bool:
            raise TEVVError("stochastic_system must be an exact bool")
        if self.stochastic_system and self.minimum_repetitions < 2:
            raise TEVVError("stochastic TEVV requires at least two repetitions")
        if type(self.evaluator_independence) is not EvaluatorIndependence:
            raise TEVVError("evaluator_independence must be an exact EvaluatorIndependence")
        for name in ("model_executed", "empirical_model_evidence", "deployment"):
            if type(getattr(self, name)) is not bool:
                raise TEVVError(f"{name} must be an exact bool")
        if self.model_executed or self.empirical_model_evidence:
            raise TEVVError("v0.1.0 profile is structural only and cannot claim model execution")
        if self.scientific_disposition != "HOLD":
            raise TEVVError("TEVV profile cannot establish scientific validity")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise TEVVError("TEVV profile cannot establish subjectivity")
        if self.consciousness_conclusion != "NOT_ESTABLISHED":
            raise TEVVError("TEVV profile cannot establish consciousness")
        if self.phenomenal_experience_conclusion != "NOT_ESTABLISHED":
            raise TEVVError("TEVV profile cannot establish phenomenal experience")
        if self.canonical_effect != "NONE" or self.deployment:
            raise TEVVError("TEVV profile cannot create canonical or deployment effect")
        _hex("profile_sha256", self.profile_sha256, 64)
        if self.profile_sha256 != _sha256(self.payload_without_digest()):
            raise TEVVError("TEVV profile content digest mismatch")

    def payload_without_digest(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "objective_ref": self.objective_ref,
            "intended_use_ref": self.intended_use_ref,
            "activities": tuple(sorted(item.value for item in self.activities)),
            "system": self.system.as_dict(),
            "metrics": [item.as_dict() for item in sorted(self.metrics, key=lambda item: item.metric_id)],
            "cases": [item.as_dict() for item in sorted(self.cases, key=lambda item: item.case_id)],
            "repetition_policy_ref": self.repetition_policy_ref,
            "nondeterminism_policy_ref": self.nondeterminism_policy_ref,
            "minimum_repetitions": self.minimum_repetitions,
            "stochastic_system": self.stochastic_system,
            "aggregation_rule_ref": self.aggregation_rule_ref,
            "evaluator_ref": self.evaluator_ref,
            "evaluator_version": self.evaluator_version,
            "evaluator_independence": self.evaluator_independence.value,
            "target_context_ref": self.target_context_ref,
            "context_similarity_statement": self.context_similarity_statement,
            "failure_action_ref": self.failure_action_ref,
            "preregistration_ref": self.preregistration_ref,
            "model_executed": self.model_executed,
            "empirical_model_evidence": self.empirical_model_evidence,
            "scientific_disposition": self.scientific_disposition,
            "subjectivity_conclusion": self.subjectivity_conclusion,
            "consciousness_conclusion": self.consciousness_conclusion,
            "phenomenal_experience_conclusion": self.phenomenal_experience_conclusion,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }


@dataclass(frozen=True, slots=True)
class TEVVProfileAssessment:
    profile_id: str
    disposition: TEVVProfileDisposition
    reasons: tuple[str, ...]
    profile_sha256: str
    model_executed: bool = False
    empirical_model_evidence: bool = False
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class AITEVVProfileGate:
    def assess(self, profile: AITEVVProfile) -> TEVVProfileAssessment:
        if type(profile) is not AITEVVProfile:
            raise TEVVError("profile must be an exact AITEVVProfile")

        reasons = [
            "SYSTEM_IDENTITY_AND_RUNTIME_BOUND",
            "TEVV_OBJECTIVE_AND_INTENDED_USE_BOUND",
            "TEST_SET_AND_DATA_QUALITY_REFS_BOUND",
            "ORACLE_STRATEGY_EXPLICIT",
            "METRICS_AND_ACCEPTANCE_CRITERIA_BOUND",
            "NONDETERMINISM_AND_REPETITION_POLICY_BOUND",
            "EVALUATOR_IDENTITY_AND_INDEPENDENCE_RECORDED",
            "TARGET_CONTEXT_AND_SIMILARITY_SCOPE_RECORDED",
            "PROFILE_IS_STRUCTURAL_NOT_EMPIRICAL_MODEL_EVIDENCE",
        ]

        if any(not case.held_out for case in profile.cases):
            reasons.append("NON_HELD_OUT_CASE_REQUIRES_REVIEW")
            return TEVVProfileAssessment(
                profile.profile_id,
                TEVVProfileDisposition.HOLD,
                tuple(reasons),
                profile.profile_sha256,
            )

        reasons.append("READY_FOR_BOUNDED_EXECUTION_NOT_MODEL_QUALITY_PASS")
        return TEVVProfileAssessment(
            profile.profile_id,
            TEVVProfileDisposition.READY_FOR_BOUNDED_EXECUTION,
            tuple(reasons),
            profile.profile_sha256,
        )


def build_tevv_profile(
    *,
    profile_id: str,
    profile_version: str,
    objective_ref: str,
    intended_use_ref: str,
    activities: tuple[TEVVActivity, ...],
    system: AISystemBinding,
    metrics: tuple[TEVVMetricSpec, ...],
    cases: tuple[TEVVCaseSpec, ...],
    repetition_policy_ref: str,
    nondeterminism_policy_ref: str,
    minimum_repetitions: int,
    stochastic_system: bool,
    aggregation_rule_ref: str,
    evaluator_ref: str,
    evaluator_version: str,
    evaluator_independence: EvaluatorIndependence,
    target_context_ref: str,
    context_similarity_statement: str,
    failure_action_ref: str,
    preregistration_ref: str,
) -> AITEVVProfile:
    values: dict[str, object] = {
        "schema_version": TEVV_PROFILE_SCHEMA_VERSION,
        "profile_id": profile_id,
        "profile_version": profile_version,
        "objective_ref": objective_ref,
        "intended_use_ref": intended_use_ref,
        "activities": tuple(sorted(item.value for item in activities)),
        "system": system.as_dict(),
        "metrics": [item.as_dict() for item in sorted(metrics, key=lambda item: item.metric_id)],
        "cases": [item.as_dict() for item in sorted(cases, key=lambda item: item.case_id)],
        "repetition_policy_ref": repetition_policy_ref,
        "nondeterminism_policy_ref": nondeterminism_policy_ref,
        "minimum_repetitions": minimum_repetitions,
        "stochastic_system": stochastic_system,
        "aggregation_rule_ref": aggregation_rule_ref,
        "evaluator_ref": evaluator_ref,
        "evaluator_version": evaluator_version,
        "evaluator_independence": evaluator_independence.value,
        "target_context_ref": target_context_ref,
        "context_similarity_statement": context_similarity_statement,
        "failure_action_ref": failure_action_ref,
        "preregistration_ref": preregistration_ref,
        "model_executed": False,
        "empirical_model_evidence": False,
        "scientific_disposition": "HOLD",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "consciousness_conclusion": "NOT_ESTABLISHED",
        "phenomenal_experience_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    return AITEVVProfile(
        profile_id=profile_id,
        profile_version=profile_version,
        objective_ref=objective_ref,
        intended_use_ref=intended_use_ref,
        activities=activities,
        system=system,
        metrics=metrics,
        cases=cases,
        repetition_policy_ref=repetition_policy_ref,
        nondeterminism_policy_ref=nondeterminism_policy_ref,
        minimum_repetitions=minimum_repetitions,
        stochastic_system=stochastic_system,
        aggregation_rule_ref=aggregation_rule_ref,
        evaluator_ref=evaluator_ref,
        evaluator_version=evaluator_version,
        evaluator_independence=evaluator_independence,
        target_context_ref=target_context_ref,
        context_similarity_statement=context_similarity_statement,
        failure_action_ref=failure_action_ref,
        preregistration_ref=preregistration_ref,
        profile_sha256=_sha256(values),
    )
