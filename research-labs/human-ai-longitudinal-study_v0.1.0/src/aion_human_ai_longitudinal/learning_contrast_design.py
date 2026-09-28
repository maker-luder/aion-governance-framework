"""Synthetic representation contrasts, composed from existing study audits.

This module checks a study *design*. It does not collect observations or infer
Human learning, retention, a CCTS-specific effect, or a causal mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .ccts_human_epistemic_agency import (
    CCTSHumanAgencyTrial,
    HumanAgencyCondition,
    ValidationHeadBinding,
    audit_ccts_human_epistemic_agency,
    ccts_manifest_snapshot_sha256,
)
from .co_constructed_thinking_space import ContributionRole
from .harness import AdmissionDisposition, StudyError
from .task_selection_exposure import (
    BoundArtifact,
    HeldOutTransferTask,
    SelectionTaskDomain,
)
from .task_selection_exposure_hardened import (
    HardenedTaskSelectionExposureAudit,
    audit_task_selection_exposure_design_hardened,
)


class RepresentationCondition(StrEnum):
    DIRECT_ANSWER = "DIRECT_ANSWER"
    REPETITION = "REPETITION"
    RE_REPRESENTATION = "RE_REPRESENTATION"
    RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT = "RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT"


class ComparatorRole(StrEnum):
    CCTS = "CCTS"
    NON_CCTS_PRACTICE = "NON_CCTS_PRACTICE"


class AssessmentTimepoint(StrEnum):
    IMMEDIATE = "IMMEDIATE"
    DELAYED = "DELAYED"


class FalsifierOutcome(StrEnum):
    UNKNOWN = "UNKNOWN"
    NULL = "NULL"
    NEGATIVE = "NEGATIVE"
    ADVERSE = "ADVERSE"


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _digest(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class LearningContrastArm:
    arm_id: str
    condition: RepresentationCondition
    comparator_role: ComparatorRole
    target_relation_stated_by: ContributionRole | None
    human_origin_relation_discovery_candidate: bool
    task_domain: SelectionTaskDomain
    task_family: BoundArtifact
    task_payload: BoundArtifact
    component_knowledge: BoundArtifact
    instruction: BoundArtifact
    exposure_content: BoundArtifact
    exposure_intensity: BoundArtifact
    prior_knowledge: BoundArtifact
    evaluator: BoundArtifact
    rubric: BoundArtifact
    provenance: BoundArtifact
    exposure_unit_id: str
    ccts_manifest_snapshot_sha256: str | None
    practice_context: BoundArtifact | None = None
    synthetic: bool = True
    contains_private_material: bool = False
    human_participant_observed: bool = False
    model_invoked: bool = False

    def __post_init__(self) -> None:
        _text("arm_id", self.arm_id)
        _text("exposure_unit_id", self.exposure_unit_id)
        if type(self.condition) is not RepresentationCondition:
            raise StudyError("condition must be an exact RepresentationCondition")
        if type(self.comparator_role) is not ComparatorRole:
            raise StudyError("comparator_role must be an exact ComparatorRole")
        if type(self.task_domain) is not SelectionTaskDomain:
            raise StudyError("task_domain must be an exact SelectionTaskDomain")
        if self.target_relation_stated_by is not None and type(self.target_relation_stated_by) is not ContributionRole:
            raise StudyError("target relation source must be an exact ContributionRole")
        if self.target_relation_stated_by not in (
            None,
            ContributionRole.HUMAN_OWNER,
            ContributionRole.AI_COLLABORATOR,
        ):
            raise StudyError("target relation source must be Human, AI, or UNKNOWN")
        for name in (
            "task_family",
            "task_payload",
            "component_knowledge",
            "instruction",
            "exposure_content",
            "exposure_intensity",
            "prior_knowledge",
            "evaluator",
            "rubric",
            "provenance",
        ):
            if type(getattr(self, name)) is not BoundArtifact:
                raise StudyError(f"{name} must be an exact BoundArtifact")
        for name in (
            "human_origin_relation_discovery_candidate",
            "synthetic",
            "contains_private_material",
            "human_participant_observed",
            "model_invoked",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic or self.human_participant_observed or self.model_invoked:
            raise StudyError("synthetic design excludes Human or model observations")
        if self.contains_private_material:
            raise StudyError("private material is excluded from synthetic design")
        if self.human_origin_relation_discovery_candidate:
            if self.target_relation_stated_by is ContributionRole.AI_COLLABORATOR:
                raise StudyError("AI-supplied relation is not Human-origin discovery")
            if (
                self.target_relation_stated_by is not ContributionRole.HUMAN_OWNER
                or self.condition is not RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT
            ):
                raise StudyError("Human-origin candidate requires Human-stated relation")
        if self.condition is RepresentationCondition.DIRECT_ANSWER and (
            self.target_relation_stated_by is not ContributionRole.AI_COLLABORATOR
        ):
            raise StudyError("DIRECT_ANSWER requires an AI-stated target relation")
        if (
            self.condition
            in (
                RepresentationCondition.REPETITION,
                RepresentationCondition.RE_REPRESENTATION,
            )
            and self.target_relation_stated_by is not None
        ):
            raise StudyError("target relation must remain unstated in this condition")
        if self.comparator_role is ComparatorRole.CCTS:
            if self.ccts_manifest_snapshot_sha256 is None:
                raise StudyError("CCTS arm requires admitted manifest snapshot")
            _digest("ccts_manifest_snapshot_sha256", self.ccts_manifest_snapshot_sha256)
            if self.practice_context is not None:
                raise StudyError("CCTS arm cannot carry non-CCTS practice context")
        else:
            if self.ccts_manifest_snapshot_sha256 is not None:
                raise StudyError("non-CCTS comparator cannot carry a CCTS snapshot")
            if type(self.practice_context) is not BoundArtifact:
                raise StudyError("non-CCTS comparator requires practice context artifact")


@dataclass(frozen=True, slots=True)
class AssessmentEvent:
    event_id: str
    arm_id: str
    timepoint: AssessmentTimepoint
    interval_minutes: int
    task_payload: BoundArtifact
    outcome: FalsifierOutcome
    synthetic: bool = True
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _text("event_id", self.event_id)
        _text("arm_id", self.arm_id)
        if type(self.timepoint) is not AssessmentTimepoint:
            raise StudyError("timepoint must be an exact AssessmentTimepoint")
        if type(self.interval_minutes) is not int:
            raise StudyError("interval_minutes must be an exact int")
        if self.timepoint is AssessmentTimepoint.IMMEDIATE:
            if self.interval_minutes != 0:
                raise StudyError("immediate interval must be zero")
        elif self.interval_minutes <= 0:
            raise StudyError("delayed interval must be positive and declared")
        if type(self.task_payload) is not BoundArtifact:
            raise StudyError("task_payload must be an exact BoundArtifact")
        if type(self.outcome) is not FalsifierOutcome:
            raise StudyError("outcome must be an exact FalsifierOutcome")
        if type(self.synthetic) is not bool or type(self.contains_private_material) is not bool:
            raise StudyError("assessment privacy flags must be exact bools")
        if not self.synthetic or self.contains_private_material:
            raise StudyError("assessment requires synthetic non-private data")


@dataclass(frozen=True, slots=True)
class LearningContrastDesign:
    arms: tuple[LearningContrastArm, ...]
    assessments: tuple[AssessmentEvent, ...]
    falsifier: BoundArtifact
    held_out_task: HeldOutTransferTask
    task_selection_audit: HardenedTaskSelectionExposureAudit
    agency_trials: tuple[CCTSHumanAgencyTrial, ...]
    agency_validation: ValidationHeadBinding
    claims_human_learning: bool = False
    claims_ccts_effect: bool = False
    claims_causal_effect: bool = False
    claims_retention_observed: bool = False
    claims_subjectivity: bool = False

    def __post_init__(self) -> None:
        if type(self.arms) is not tuple or any(type(item) is not LearningContrastArm for item in self.arms):
            raise StudyError("arms must be exact LearningContrastArm values")
        if type(self.assessments) is not tuple or any(type(item) is not AssessmentEvent for item in self.assessments):
            raise StudyError("assessments must be exact AssessmentEvent values")
        if type(self.falsifier) is not BoundArtifact:
            raise StudyError("falsifier must be an exact BoundArtifact")
        if type(self.held_out_task) is not HeldOutTransferTask:
            raise StudyError("held_out_task must be an exact HeldOutTransferTask")
        if type(self.task_selection_audit) is not HardenedTaskSelectionExposureAudit:
            raise StudyError("task_selection_audit must be an exact existing audit")
        if type(self.agency_trials) is not tuple or any(
            type(item) is not CCTSHumanAgencyTrial for item in self.agency_trials
        ):
            raise StudyError("agency_trials must be exact CCTSHumanAgencyTrial values")
        if type(self.agency_validation) is not ValidationHeadBinding:
            raise StudyError("agency_validation must be an exact ValidationHeadBinding")
        for name in (
            "claims_human_learning",
            "claims_ccts_effect",
            "claims_causal_effect",
            "claims_retention_observed",
            "claims_subjectivity",
        ):
            value = getattr(self, name)
            if type(value) is not bool:
                raise StudyError(f"{name} must be an exact bool")
            if value:
                raise StudyError("scientific claims are excluded from structural design")


@dataclass(frozen=True, slots=True)
class LearningContrastAudit:
    complete_design: bool
    comparator_present: bool
    falsifier_bound: bool
    timepoint_integrity: bool
    held_out_contamination_control: bool
    task_selection_controls_revalidated: bool
    agency_bindings_revalidated: bool
    human_learning: str = "NOT_ESTABLISHED"
    ccts_effect: str = "NOT_ESTABLISHED"
    retention_observed: str = "NOT_ESTABLISHED"
    causal_effect: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    mode: str = "DETERMINISTIC_SYNTHETIC_STUDY_DESIGN"


def audit_learning_contrast_design(design: LearningContrastDesign) -> LearningContrastAudit:
    """Re-audit inherited controls before checking the new matched contrast."""
    if type(design) is not LearningContrastDesign:
        raise StudyError("design must be an exact LearningContrastDesign")
    exposure = design.task_selection_audit
    verified_exposure = audit_task_selection_exposure_design_hardened(
        exposure.units,
        exposure.choice_opportunity_traces,
        exposure.execution_identities,
        exposure.within_family_held_out_tasks,
        exposure.cross_family_held_out_tasks,
    )
    if exposure != verified_exposure:
        raise StudyError("task-selection audit does not match recomputed controls")
    agency = audit_ccts_human_epistemic_agency(design.agency_trials, design.agency_validation)
    if not agency.complete_design or not agency.held_out_contamination_control:
        raise StudyError("CCTS Human agency bindings are incomplete")
    if len({item.unit_id for item in design.agency_trials}) != 1:
        raise StudyError("contrast must bind exactly one Human agency unit")
    assisted = next(item for item in design.agency_trials if item.condition is HumanAgencyCondition.CCTS_AI_AVAILABLE)
    held_out_agency = next(
        item for item in design.agency_trials if item.condition is HumanAgencyCondition.AI_WITHHELD_HELD_OUT
    )
    if assisted.ccts_manifest is None:
        raise StudyError("admitted CCTS manifest is required")
    snapshot = ccts_manifest_snapshot_sha256(assisted.ccts_manifest)
    if design.held_out_task not in exposure.within_family_held_out_tasks:
        raise StudyError("held-out task must bind a verified selection-control task")
    if held_out_agency.task_payload_sha256 != design.held_out_task.task_payload_artifact.sha256_digest:
        raise StudyError("held-out task must bind the Human agency held-out payload")

    arms = design.arms
    if len({arm.arm_id for arm in arms}) != len(arms):
        raise StudyError("contrast arm IDs must be unique")
    ccts_arms = tuple(arm for arm in arms if arm.comparator_role is ComparatorRole.CCTS)
    comparators = tuple(arm for arm in arms if arm.comparator_role is ComparatorRole.NON_CCTS_PRACTICE)
    if len(comparators) != 1 or comparators[0].condition is not (
        RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT
    ):
        raise StudyError("matched non-CCTS practice comparator is required")
    practice_context = comparators[0].practice_context
    if practice_context is None or practice_context.sha256_digest in {
        arm.instruction.sha256_digest for arm in ccts_arms
    }:
        raise StudyError("comparator requires independent practice context content")
    if len(ccts_arms) != 4 or {arm.condition for arm in ccts_arms} != set(RepresentationCondition):
        raise StudyError("exactly four CCTS representation conditions are required")
    if len({arm.instruction.sha256_digest for arm in ccts_arms}) != 4:
        raise StudyError("four condition instruction content digests must be distinct")
    for arm in ccts_arms:
        if arm.ccts_manifest_snapshot_sha256 != snapshot:
            raise StudyError("CCTS arm must bind admitted manifest snapshot")
    for arm in arms:
        if arm.provenance.sha256_digest != assisted.ccts_manifest.provenance_manifest_sha256:
            raise StudyError("source-role provenance binding drift")
        if arm.task_payload.sha256_digest != assisted.task_payload_sha256:
            raise StudyError("task payload must bind Human agency task")
        if arm.evaluator.sha256_digest != assisted.evaluator_sha256:
            raise StudyError("evaluator binding drift from Human agency audit")
        if arm.rubric.sha256_digest != assisted.scoring_rubric_sha256:
            raise StudyError("rubric binding drift from Human agency audit")

    base = arms[0]
    matched = (
        ("task_domain", "task domain"),
        ("task_family", "task family"),
        ("task_payload", "task payload"),
        ("component_knowledge", "component knowledge"),
        ("exposure_content", "exposure content"),
        ("exposure_intensity", "exposure intensity"),
        ("prior_knowledge", "prior knowledge"),
        ("evaluator", "evaluator"),
        ("rubric", "rubric"),
        ("exposure_unit_id", "exposure unit"),
    )
    for name, label in matched:
        if any(getattr(arm, name) != getattr(base, name) for arm in arms[1:]):
            raise StudyError(f"matched {label} drift")
    units = {unit.unit_id: unit for unit in exposure.units}
    unit = units.get(base.exposure_unit_id)
    if unit is None:
        raise StudyError("exposure unit must bind a verified task-selection unit")
    if (
        unit.prior_knowledge_control != base.prior_knowledge
        or unit.evaluator_payload != base.evaluator
        or unit.exposure_unit_definition != base.exposure_intensity
    ):
        raise StudyError("task-selection control binding drift")
    if not any(
        event.task_domain is base.task_domain
        and event.task_family_artifact == base.task_family
        and event.exposure_payload_artifact == base.exposure_content
        for event in unit.realized_exposure_trace
    ):
        raise StudyError("exposure content must bind a verified task-domain episode")

    held_out_digest = design.held_out_task.task_payload_artifact.sha256_digest
    if design.held_out_task.task_domain is not base.task_domain or (
        design.held_out_task.task_family_artifact != base.task_family
    ):
        raise StudyError("held-out task domain/family drift")
    prior_content = (
        {arm.task_payload.sha256_digest for arm in arms}
        | {arm.exposure_content.sha256_digest for arm in arms}
        | {arm.component_knowledge.sha256_digest for arm in arms}
        | {arm.instruction.sha256_digest for arm in arms}
    )
    prior_content.update(item.payload_sha256 for item in assisted.ccts_manifest.contributions)
    if held_out_digest in prior_content:
        raise StudyError("held-out payload duplicates prior exposure content")

    events = design.assessments
    if len(events) != 2 * len(arms) or len({event.event_id for event in events}) != len(events):
        raise StudyError("assessment event IDs must be distinct and complete")
    for arm in arms:
        own = tuple(event for event in events if event.arm_id == arm.arm_id)
        if len(own) != 2 or {event.timepoint for event in own} != set(AssessmentTimepoint):
            raise StudyError("each arm requires immediate and delayed assessments")
        if any(event.task_payload != arm.task_payload for event in own):
            raise StudyError("assessment task payload binding drift")
    if len({event.interval_minutes for event in events if event.timepoint is AssessmentTimepoint.DELAYED}) != 1:
        raise StudyError("delayed interval must be matched across arms")
    if any(event.arm_id not in {arm.arm_id for arm in arms} for event in events):
        raise StudyError("assessment refers to an unknown arm")

    return LearningContrastAudit(
        complete_design=True,
        comparator_present=True,
        falsifier_bound=True,
        timepoint_integrity=True,
        held_out_contamination_control=True,
        task_selection_controls_revalidated=True,
        agency_bindings_revalidated=True,
    )
