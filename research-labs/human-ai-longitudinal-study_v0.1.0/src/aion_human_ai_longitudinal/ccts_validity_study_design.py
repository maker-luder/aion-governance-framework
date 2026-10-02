"""Synthetic study-design records for the two CCTS validity questions.

This module reuses the harness's error/disposition types. It neither scores
transcripts nor consumes participant observations; digest declarations do not
authenticate a protocol, coding manual, or outcome measurement.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from .ccts_human_epistemic_agency import HumanAgencyCondition
from .harness import AdmissionDisposition, StudyError

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class NeighborConstruct(StrEnum):
    ORDINARY_ASSISTANT = "ORDINARY_ASSISTANT"
    PROMPT_REFINEMENT = "PROMPT_REFINEMENT"
    INSTRUCT_SERVE_REPEAT = "INSTRUCT_SERVE_REPEAT"
    ITERATIVE_PROMPTING = "ITERATIVE_PROMPTING"
    ORDINARY_ITERATIVE_DIALOGUE = "ORDINARY_ITERATIVE_DIALOGUE"
    COGNITIVE_COLLABORATIVE_DIALOGUE = "COGNITIVE_COLLABORATIVE_DIALOGUE"
    SOCIALLY_SHARED_REGULATION = "SOCIALLY_SHARED_REGULATION"
    CO_REGULATION = "CO_REGULATION"
    HUMAN_AI_TEAMING = "HUMAN_AI_TEAMING"
    DISTRIBUTED_COGNITION = "DISTRIBUTED_COGNITION"
    SHARED_MENTAL_MODELS = "SHARED_MENTAL_MODELS"
    EPISTEMIC_CO_AGENCY = "EPISTEMIC_CO_AGENCY"


class HybridNegative(StrEnum):
    PROVENANCE_AUTHORITY_WITHOUT_RECIPROCAL_REVISION = "PROVENANCE_AUTHORITY_WITHOUT_RECIPROCAL_REVISION"
    RECIPROCAL_REVISION_WITHOUT_RECONSTRUCTABLE_PROVENANCE = "RECIPROCAL_REVISION_WITHOUT_RECONSTRUCTABLE_PROVENANCE"


class OutcomeCondition(StrEnum):
    CCTS = "CCTS"
    MATCHED_NON_CCTS = "MATCHED_NON_CCTS"
    HUMAN_ALONE = "HUMAN_ALONE"
    AI_ALONE = "AI_ALONE"


class OutcomeMeasure(StrEnum):
    INDEPENDENT_HUMAN_JUDGMENT = "INDEPENDENT_HUMAN_JUDGMENT"
    INDEPENDENT_RECONSTRUCTION = "INDEPENDENT_RECONSTRUCTION"
    ERROR_DETECTION = "ERROR_DETECTION"
    CALIBRATION = "CALIBRATION"
    IMMEDIATE_TASK_PERFORMANCE = "IMMEDIATE_TASK_PERFORMANCE"
    DELAYED_RETENTION = "DELAYED_RETENTION"
    HELD_OUT_TRANSFER = "HELD_OUT_TRANSFER"


class AssessmentSourceRole(StrEnum):
    HUMAN_PARTICIPANT = "HUMAN_PARTICIPANT"
    AI = "AI"
    HUMAN_AI = "HUMAN_AI"


def _ids(name: str, values: tuple[str, ...], minimum: int = 1) -> None:
    if type(values) is not tuple or len(values) < minimum:
        raise StudyError(f"{name} requires at least {minimum} independent coders" if name == "independent_coder_ids" else f"{name} requires at least {minimum} IDs")
    if any(type(value) is not str or not value.strip() for value in values):
        raise StudyError(f"{name} requires non-empty text IDs")
    if len(set(values)) != len(values):
        raise StudyError(f"{name} IDs must be unique")


def _digest(name: str, value: str | None) -> None:
    if value is not None and (type(value) is not str or _SHA256.fullmatch(value) is None):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class DiscriminantPlan:
    candidate_unit_ids: tuple[str, ...]
    hard_negative_cases: tuple[tuple[NeighborConstruct, str], ...]
    hybrid_negative_cases: tuple[tuple[HybridNegative, str], ...]
    coding_manual_sha256: str | None
    falsification_rule_sha256: str | None
    independent_coder_ids: tuple[str, ...]
    coders_blind_to_candidate_label: bool
    coders_blind_to_outcome: bool

    def __post_init__(self) -> None:
        _ids("candidate_unit_ids", self.candidate_unit_ids)
        if type(self.hard_negative_cases) is not tuple or not self.hard_negative_cases:
            raise StudyError("hard_negative_cases must be a non-empty tuple")
        for case in self.hard_negative_cases:
            if type(case) is not tuple or len(case) != 2 or type(case[0]) is not NeighborConstruct:
                raise StudyError("hard-negative cases require exact NeighborConstruct values")
            if type(case[1]) is not str or not case[1].strip():
                raise StudyError("hard-negative cases require non-empty unit IDs")
        if type(self.hybrid_negative_cases) is not tuple:
            raise StudyError("hybrid_negative_cases must be an exact tuple")
        for hybrid_case in self.hybrid_negative_cases:
            if type(hybrid_case) is not tuple or len(hybrid_case) != 2 or type(hybrid_case[0]) is not HybridNegative:
                raise StudyError("hybrid-negative cases require exact HybridNegative values")
            if type(hybrid_case[1]) is not str or not hybrid_case[1].strip():
                raise StudyError("hybrid-negative cases require non-empty unit IDs")
        negative_ids = [unit for _, unit in self.hard_negative_cases + self.hybrid_negative_cases]
        if len(set(negative_ids)) != len(negative_ids):
            raise StudyError("hard-negative case unit IDs must be unique")
        if set(self.candidate_unit_ids) & set(negative_ids):
            raise StudyError("candidate and hard-negative unit IDs must be disjoint")
        _digest("coding_manual_sha256", self.coding_manual_sha256)
        _digest("falsification_rule_sha256", self.falsification_rule_sha256)
        _ids("independent_coder_ids", self.independent_coder_ids, minimum=2)
        for name in ("coders_blind_to_candidate_label", "coders_blind_to_outcome"):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")


@dataclass(frozen=True, slots=True)
class OutcomePlan:
    condition_unit_ids: tuple[tuple[OutcomeCondition, str], ...]
    primary_measure: OutcomeMeasure
    scoring_rule_sha256: str | None
    held_out_task_sha256: str | None
    independent_rater_ids: tuple[str, ...]
    raters_blind_to_ccts_status: bool
    exposure_matching_plan_sha256: str | None
    baseline_covariate_plan_sha256: str | None
    ai_quality_record_plan_sha256: str | None
    assessment_delay_minutes: int | None
    primary_assessment_condition: HumanAgencyCondition
    primary_response_source: AssessmentSourceRole

    def __post_init__(self) -> None:
        if type(self.condition_unit_ids) is not tuple or not self.condition_unit_ids:
            raise StudyError("condition_unit_ids must be a non-empty tuple")
        for pair in self.condition_unit_ids:
            if type(pair) is not tuple or len(pair) != 2 or type(pair[0]) is not OutcomeCondition:
                raise StudyError("condition_unit_ids require exact OutcomeCondition values")
            if type(pair[1]) is not str or not pair[1].strip():
                raise StudyError("condition_unit_ids require non-empty unit IDs")
        if len({condition for condition, _ in self.condition_unit_ids}) != len(self.condition_unit_ids):
            raise StudyError("each OutcomeCondition must have one unit ID")
        if len({unit for _, unit in self.condition_unit_ids}) != len(self.condition_unit_ids):
            raise StudyError("conditions require a distinct unit ID")
        if type(self.primary_measure) is not OutcomeMeasure:
            raise StudyError("primary_measure must be an exact OutcomeMeasure, excluding structural status")
        if type(self.primary_assessment_condition) is not HumanAgencyCondition:
            raise StudyError("primary_assessment_condition must be an exact HumanAgencyCondition")
        if type(self.primary_response_source) is not AssessmentSourceRole:
            raise StudyError("primary_response_source must be an exact AssessmentSourceRole")
        for name in (
            "scoring_rule_sha256",
            "held_out_task_sha256",
            "exposure_matching_plan_sha256",
            "baseline_covariate_plan_sha256",
            "ai_quality_record_plan_sha256",
        ):
            _digest(name, getattr(self, name))
        _ids("independent_rater_ids", self.independent_rater_ids, minimum=2)
        if type(self.raters_blind_to_ccts_status) is not bool:
            raise StudyError("raters_blind_to_ccts_status must be an exact bool")
        if self.assessment_delay_minutes is not None and (
            type(self.assessment_delay_minutes) is not int or self.assessment_delay_minutes <= 0
        ):
            raise StudyError("assessment_delay_minutes must be a positive exact int")


@dataclass(frozen=True, slots=True)
class CCTSValidityStudyDesign:
    study_id: str
    discriminant: DiscriminantPlan
    outcome: OutcomePlan
    claims_ccts_validation: bool = False
    claims_human_learning: bool = False
    claims_retention: bool = False
    claims_transfer: bool = False
    claims_ccts_specific_effect: bool = False
    claims_causality: bool = False
    claims_human_ai_synergy: bool = False

    def __post_init__(self) -> None:
        if type(self.study_id) is not str or not self.study_id.strip():
            raise StudyError("study_id must be non-empty text")
        if type(self.discriminant) is not DiscriminantPlan or type(self.outcome) is not OutcomePlan:
            raise StudyError("study design requires exact DiscriminantPlan and OutcomePlan")
        if set(self.discriminant.independent_coder_ids) & set(self.outcome.independent_rater_ids):
            raise StudyError("discriminant coders and outcome raters must be disjoint")
        for name in (
            "claims_ccts_validation", "claims_human_learning", "claims_retention",
            "claims_transfer", "claims_ccts_specific_effect", "claims_causality",
            "claims_human_ai_synergy",
        ):
            value = getattr(self, name)
            if type(value) is not bool:
                raise StudyError(f"{name} must be an exact bool")
            if value:
                raise StudyError("scientific claims cannot be promoted by a study-design record")


@dataclass(frozen=True, slots=True)
class CCTSValidityStudyAudit:
    study_id: str
    discriminant_plan_complete: bool
    outcome_plan_complete: bool
    empirical_observations_present: bool = False
    ccts_validation: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    retention: str = "NOT_ESTABLISHED"
    transfer: str = "NOT_ESTABLISHED"
    ccts_specific_effect: str = "NOT_ESTABLISHED"
    causality: str = "NOT_ESTABLISHED"
    human_ai_synergy: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    mode: str = "SYNTHETIC_STUDY_DESIGN_ONLY"

    def __post_init__(self) -> None:
        if type(self.study_id) is not str or not self.study_id.strip():
            raise StudyError("study_id must be non-empty text")
        if type(self.discriminant_plan_complete) is not bool or type(self.outcome_plan_complete) is not bool:
            raise StudyError("coverage flags must be exact bools")
        fixed = (
            self.empirical_observations_present is False
            and all(
                getattr(self, name) == "NOT_ESTABLISHED"
                for name in (
                    "ccts_validation", "human_learning", "retention", "transfer",
                    "ccts_specific_effect", "causality", "human_ai_synergy",
                )
            )
            and self.scientific_disposition is AdmissionDisposition.HOLD
            and self.canonical_effect == "NONE"
            and self.deployment is False
            and self.mode == "SYNTHETIC_STUDY_DESIGN_ONLY"
        )
        if not fixed:
            raise StudyError("fixed scientific boundary cannot be promoted by audit construction")


def audit_ccts_validity_study_design(design: CCTSValidityStudyDesign) -> CCTSValidityStudyAudit:
    """Report declared design-field coverage, never empirical validity or readiness."""
    if type(design) is not CCTSValidityStudyDesign:
        raise StudyError("design must be an exact CCTSValidityStudyDesign")
    discriminant = design.discriminant
    outcome = design.outcome
    independent_human_measure = outcome.primary_measure is not OutcomeMeasure.IMMEDIATE_TASK_PERFORMANCE
    human_only_assessment = (
        outcome.primary_response_source is AssessmentSourceRole.HUMAN_PARTICIPANT
        and outcome.primary_assessment_condition in {
            HumanAgencyCondition.AI_WITHHELD_JUDGMENT,
            HumanAgencyCondition.AI_WITHHELD_HELD_OUT,
        }
    )
    return CCTSValidityStudyAudit(
        study_id=design.study_id,
        discriminant_plan_complete=(
            {neighbor for neighbor, _ in discriminant.hard_negative_cases} == set(NeighborConstruct)
            and {kind for kind, _ in discriminant.hybrid_negative_cases} == set(HybridNegative)
            and discriminant.coding_manual_sha256 is not None
            and discriminant.falsification_rule_sha256 is not None
            and discriminant.coders_blind_to_candidate_label
            and discriminant.coders_blind_to_outcome
        ),
        outcome_plan_complete=(
            {condition for condition, _ in outcome.condition_unit_ids} == set(OutcomeCondition)
            and outcome.scoring_rule_sha256 is not None
            and outcome.held_out_task_sha256 is not None
            and outcome.exposure_matching_plan_sha256 is not None
            and outcome.baseline_covariate_plan_sha256 is not None
            and outcome.ai_quality_record_plan_sha256 is not None
            and outcome.raters_blind_to_ccts_status
            and (not independent_human_measure or human_only_assessment)
            and (
                outcome.primary_measure is not OutcomeMeasure.HELD_OUT_TRANSFER
                or outcome.primary_assessment_condition is HumanAgencyCondition.AI_WITHHELD_HELD_OUT
            )
            and (
                outcome.primary_measure is not OutcomeMeasure.DELAYED_RETENTION
                or outcome.assessment_delay_minutes is not None
            )
        ),
    )
