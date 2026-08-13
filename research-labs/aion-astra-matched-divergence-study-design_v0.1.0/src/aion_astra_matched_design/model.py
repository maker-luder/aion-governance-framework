from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class StudyStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    HOLD = "HOLD"


class SourceStatus(StrEnum):
    CURRENT_VERIFIED = "CURRENT_VERIFIED"
    HISTORICAL = "HISTORICAL"
    UNVERIFIED = "UNVERIFIED"


class ExecutionState(StrEnum):
    PROHIBITED = "PROHIBITED"
    NOT_STARTED = "NOT_STARTED"
    OBSERVED = "OBSERVED"


class ComparisonMode(StrEnum):
    PAIRED = "PAIRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class SystemSource:
    system_id: str
    family: str
    component_ref: str | None
    version_ref: str | None
    source_state_ref: str | None
    source_status: SourceStatus
    environment_ref: str | None


@dataclass(frozen=True, slots=True)
class StimulusPair:
    pair_id: str
    stimulus_digest: str | None
    context_digest: str | None
    prompt_version: str | None
    expected_exposure_count: int | None
    control_exposure_count: int | None
    order_assignment: str | None


@dataclass(frozen=True, slots=True)
class StudyDesign:
    study_id: str
    protocol_version: str
    research_question_ref: str | None
    estimand_ref: str | None
    comparison_mode: ComparisonMode
    aion_source: SystemSource
    astra_source: SystemSource
    source_evidence_refs: tuple[str, ...]
    tested_source_head: str | None
    reporting_head: str | None
    preregistration_ref: str | None
    immutable_plan_digest: str | None
    outcome_scope: str | None
    comparison_rule_ref: str | None
    outcome_blinding_ref: str | None
    evaluator_identity_sealed: bool
    randomization_ref: str | None
    counterbalance_ref: str | None
    leakage_attestation_ref: str | None
    stopping_rule_ref: str | None
    execution_prohibition_ref: str | None
    environment_ref: str | None
    stimulus_pairs: tuple[StimulusPair, ...]
    model_execution: bool = False
    observed_result_ref: str | None = None
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False


@dataclass(frozen=True, slots=True)
class StudyDecision:
    status: StudyStatus
    disposition: Disposition
    reason: str
    study_id: str
    missing_fields: tuple[str, ...] = ()
    contradiction_fields: tuple[str, ...] = ()
    execution_state: ExecutionState = ExecutionState.PROHIBITED
    observed_result: str = "NOT_EVALUATED"
    tested_source_head: str | None = None
    reporting_head: str | None = None
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        payload["execution_state"] = self.execution_state.value
        return payload


def _missing(values: dict[str, object]) -> tuple[str, ...]:
    return tuple(key for key, value in values.items() if value is None or value == "" or value == ())


def _decision(
    design: StudyDesign,
    status: StudyStatus,
    disposition: Disposition,
    reason: str,
    *,
    missing: tuple[str, ...] = (),
    contradictions: tuple[str, ...] = (),
    execution_state: ExecutionState = ExecutionState.PROHIBITED,
    observed_result: str = "NOT_EVALUATED",
) -> StudyDecision:
    return StudyDecision(
        status=status,
        disposition=disposition,
        reason=reason,
        study_id=design.study_id,
        missing_fields=missing,
        contradiction_fields=contradictions,
        execution_state=execution_state,
        observed_result=observed_result,
        tested_source_head=design.tested_source_head,
        reporting_head=design.reporting_head,
        canonical_effect=design.canonical_effect,
        governance_effect=design.governance_effect,
        deployment=design.deployment,
    )


def _source_missing(prefix: str, source: SystemSource) -> dict[str, object]:
    return {
        f"{prefix}.system_id": source.system_id,
        f"{prefix}.family": source.family,
        f"{prefix}.component_ref": source.component_ref,
        f"{prefix}.version_ref": source.version_ref,
        f"{prefix}.source_state_ref": source.source_state_ref,
        f"{prefix}.environment_ref": source.environment_ref,
    }


def audit_study_design(design: StudyDesign) -> StudyDecision:
    """Audit design metadata only; never executes AION or Astra."""
    if design.canonical_effect != "NONE" or design.governance_effect != "NONE" or design.deployment:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "BOUNDARY_EFFECT_REQUESTED")
    if design.model_execution:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "MODEL_EXECUTION_FORBIDDEN", execution_state=ExecutionState.OBSERVED)
    if design.observed_result_ref is not None:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "OBSERVED_RESULT_PRESENT_IN_DESIGN_ONLY_STUDY", observed_result="OBSERVED")
    required = {
        "study_id": design.study_id,
        "protocol_version": design.protocol_version,
        "research_question_ref": design.research_question_ref,
        "estimand_ref": design.estimand_ref,
        "tested_source_head": design.tested_source_head,
        "source_evidence_refs": design.source_evidence_refs,
        "preregistration_ref": design.preregistration_ref,
        "immutable_plan_digest": design.immutable_plan_digest,
        "outcome_scope": design.outcome_scope,
        "comparison_rule_ref": design.comparison_rule_ref,
        "outcome_blinding_ref": design.outcome_blinding_ref,
        "randomization_ref": design.randomization_ref,
        "counterbalance_ref": design.counterbalance_ref,
        "leakage_attestation_ref": design.leakage_attestation_ref,
        "stopping_rule_ref": design.stopping_rule_ref,
        "execution_prohibition_ref": design.execution_prohibition_ref,
        "environment_ref": design.environment_ref,
    }
    missing = _missing(required)
    missing_values = {**required, **_source_missing("aion_source", design.aion_source), **_source_missing("astra_source", design.astra_source)}
    missing += _missing(missing_values)
    if missing:
        return _decision(design, StudyStatus.INDETERMINATE, Disposition.HOLD, "STUDY_METADATA_INCOMPLETE", missing=tuple(dict.fromkeys(missing)))
    if design.tested_source_head != design.aion_source.source_state_ref or design.tested_source_head != design.astra_source.source_state_ref:
        return _decision(
            design,
            StudyStatus.INVALID,
            Disposition.HOLD,
            "SOURCE_STATE_HEAD_MISMATCH",
            contradictions=("tested_source_head", "aion_source.source_state_ref", "astra_source.source_state_ref"),
        )
    if design.reporting_head and design.reporting_head == design.tested_source_head:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "REPORTING_HEAD_MISLABELED_AS_TESTED_HEAD", contradictions=("reporting_head", "tested_source_head"))
    if design.reporting_head and design.reporting_head == design.aion_source.source_state_ref:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "REPORTING_HEAD_MISLABELED_AS_TESTED_HEAD", contradictions=("reporting_head", "aion_source.source_state_ref"))
    if design.aion_source.family != "AION" or design.astra_source.family != "ASTRA":
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "SYSTEM_FAMILY_MISMATCH", contradictions=("aion_source.family", "astra_source.family"))
    if design.aion_source.system_id == design.astra_source.system_id or design.aion_source.component_ref == design.astra_source.component_ref:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "SYSTEM_REFERENCES_COLLIDE", contradictions=("aion_source", "astra_source"))
    if design.aion_source.environment_ref != design.astra_source.environment_ref or design.environment_ref != design.aion_source.environment_ref:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "ENVIRONMENT_REFERENCE_MISMATCH", contradictions=("environment_ref",))
    if design.aion_source.source_status is not SourceStatus.CURRENT_VERIFIED or design.astra_source.source_status is not SourceStatus.CURRENT_VERIFIED:
        return _decision(design, StudyStatus.INDETERMINATE, Disposition.HOLD, "SOURCE_STATUS_NOT_CURRENT_VERIFIED")
    prohibited_outcome_terms = ("subjectivity", "consciousness", "identity", "moral status", "phenomenal")
    if any(term in design.outcome_scope.lower() for term in prohibited_outcome_terms):
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "OUTCOME_SCOPE_EXCEEDS_MECHANISM_STUDY", contradictions=("outcome_scope",))
    if not design.stimulus_pairs:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "NO_STIMULUS_PAIRS_DECLARED")
    pair_ids = {pair.pair_id for pair in design.stimulus_pairs}
    if len(pair_ids) != len(design.stimulus_pairs):
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "DUPLICATE_STIMULUS_PAIR_ID")
    for pair in design.stimulus_pairs:
        pair_required = {
            f"pair[{pair.pair_id}].stimulus_digest": pair.stimulus_digest,
            f"pair[{pair.pair_id}].context_digest": pair.context_digest,
            f"pair[{pair.pair_id}].prompt_version": pair.prompt_version,
            f"pair[{pair.pair_id}].expected_exposure_count": pair.expected_exposure_count,
            f"pair[{pair.pair_id}].control_exposure_count": pair.control_exposure_count,
            f"pair[{pair.pair_id}].order_assignment": pair.order_assignment,
        }
        pair_missing = _missing(pair_required)
        if pair_missing:
            return _decision(design, StudyStatus.INDETERMINATE, Disposition.HOLD, "STIMULUS_PAIR_METADATA_INCOMPLETE", missing=pair_missing)
        assert pair.expected_exposure_count is not None and pair.control_exposure_count is not None
        if pair.expected_exposure_count != pair.control_exposure_count:
            return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "EXPOSURE_BUDGET_UNEQUAL", contradictions=(f"pair[{pair.pair_id}].exposure",))
        if pair.expected_exposure_count < 1:
            return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "NON_POSITIVE_EXPOSURE_BUDGET", contradictions=(f"pair[{pair.pair_id}].exposure",))
    prompt_versions = {pair.prompt_version for pair in design.stimulus_pairs}
    if len(prompt_versions) != 1:
        return _decision(design, StudyStatus.INVALID, Disposition.HOLD, "STIMULUS_PROMPT_VERSION_DRIFT")
    if design.comparison_mode is ComparisonMode.PAIRED:
        orders = {pair.order_assignment for pair in design.stimulus_pairs if pair.order_assignment}
        if not any("AB" in order for order in orders) or not any("BA" in order for order in orders):
            return _decision(design, StudyStatus.INDETERMINATE, Disposition.HOLD, "COUNTERBALANCE_INCOMPLETE")
    if not design.evaluator_identity_sealed:
        return _decision(design, StudyStatus.INDETERMINATE, Disposition.HOLD, "EVALUATOR_IDENTITY_NOT_SEALED")
    return _decision(design, StudyStatus.COMPLETE, Disposition.ADMISSIBLE_FOR_REVIEW, "AION_ASTRA_STUDY_DESIGN_COMPLETE")
