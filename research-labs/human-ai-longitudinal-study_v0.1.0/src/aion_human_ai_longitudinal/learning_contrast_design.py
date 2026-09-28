"""Synthetic representation contrasts, composed from existing study audits.

This module checks a study *design*. It does not collect observations or infer
Human learning, retention, a CCTS-specific effect, or a causal mechanism.
"""

from __future__ import annotations

import json

from dataclasses import dataclass
from enum import StrEnum

from .ccts_human_epistemic_agency import (
    CCTSHumanAgencyTrial,
    HumanAgencyCondition,
    ValidationHeadBinding,
    audit_ccts_human_epistemic_agency,
    ccts_manifest_snapshot_sha256,
)
from .harness import AdmissionDisposition, StudyError
from .task_selection_exposure import (
    BoundArtifact,
    HeldOutTransferTask,
    SelectionTaskDomain,
)
from .task_selection_exposure_hardened import (
    ExecutionIdentityBinding,
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


class RelationSourceRole(StrEnum):
    HUMAN = "HUMAN"
    AI = "AI"
    UNKNOWN = "UNKNOWN"


class ComponentTransform(StrEnum):
    ORIGINAL = "ORIGINAL"
    VERBATIM_REPEAT = "VERBATIM_REPEAT"
    REORGANIZE_EXISTING = "REORGANIZE_EXISTING"


class RelationVisibility(StrEnum):
    PRESENTED = "PRESENTED"
    WITHHELD = "WITHHELD"


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
class ComponentInformation:
    component_id: str
    payload: BoundArtifact

    def __post_init__(self) -> None:
        _text("component_id", self.component_id)
        if type(self.payload) is not BoundArtifact:
            raise StudyError("component payload must be an exact BoundArtifact")


@dataclass(frozen=True, slots=True)
class PresentationPlan:
    component_ids: tuple[str, ...]
    component_transform: ComponentTransform
    relation_visibility: RelationVisibility
    relation_source_role: RelationSourceRole
    human_judgment_required: bool

    def __post_init__(self) -> None:
        if type(self.component_ids) is not tuple or not self.component_ids:
            raise StudyError("presentation component_ids must be an exact non-empty tuple")
        if any(type(item) is not str or not item.strip() for item in self.component_ids):
            raise StudyError("presentation component IDs must be non-empty text")
        if len(set(self.component_ids)) != len(self.component_ids):
            raise StudyError("presentation component IDs must be unique")
        if type(self.component_transform) is not ComponentTransform:
            raise StudyError("component_transform must be an exact ComponentTransform")
        if type(self.relation_visibility) is not RelationVisibility:
            raise StudyError("relation_visibility must be an exact RelationVisibility")
        if type(self.relation_source_role) is not RelationSourceRole:
            raise StudyError("relation_source_role must be an exact RelationSourceRole")
        if type(self.human_judgment_required) is not bool:
            raise StudyError("human_judgment_required must be an exact bool")
        if self.relation_visibility is RelationVisibility.WITHHELD:
            if self.relation_source_role is not RelationSourceRole.UNKNOWN:
                raise StudyError("withheld relation must not assert a Human or AI source")
        elif self.relation_source_role is RelationSourceRole.UNKNOWN:
            raise StudyError("presented relation requires an explicit source role")


def render_practice_protocol(
    presentation: PresentationPlan,
    execution_identity: ExecutionIdentityBinding,
) -> str:
    if type(presentation) is not PresentationPlan:
        raise StudyError("practice presentation must be an exact PresentationPlan")
    if type(execution_identity) is not ExecutionIdentityBinding:
        raise StudyError("practice execution identity must be an exact ExecutionIdentityBinding")
    payload = {
        "component_ids": list(presentation.component_ids),
        "component_transform": presentation.component_transform.value,
        "execution_id": execution_identity.execution_id,
        "execution_record_artifact_id": execution_identity.execution_record_artifact_id,
        "human_judgment_required": presentation.human_judgment_required,
        "relation_source_role": presentation.relation_source_role.value,
        "relation_visibility": presentation.relation_visibility.value,
        "unit_id": execution_identity.unit_id,
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


@dataclass(frozen=True, slots=True)
class LearningContrastArm:
    arm_id: str
    condition: RepresentationCondition
    comparator_role: ComparatorRole
    presentation: PresentationPlan
    task_domain: SelectionTaskDomain
    task_family: BoundArtifact
    task_payload: BoundArtifact
    exposure_content: BoundArtifact
    exposure_intensity: BoundArtifact
    prior_knowledge: BoundArtifact
    evaluator: BoundArtifact
    rubric: BoundArtifact
    provenance: BoundArtifact
    execution_identity: ExecutionIdentityBinding
    ccts_manifest_snapshot_sha256: str | None
    practice_protocol: BoundArtifact | None = None
    synthetic: bool = True
    contains_private_material: bool = False
    human_participant_observed: bool = False
    model_invoked: bool = False

    def __post_init__(self) -> None:
        _text("arm_id", self.arm_id)
        if type(self.condition) is not RepresentationCondition:
            raise StudyError("condition must be an exact RepresentationCondition")
        if type(self.comparator_role) is not ComparatorRole:
            raise StudyError("comparator_role must be an exact ComparatorRole")
        if type(self.presentation) is not PresentationPlan:
            raise StudyError("presentation must be an exact PresentationPlan")
        if type(self.task_domain) is not SelectionTaskDomain:
            raise StudyError("task_domain must be an exact SelectionTaskDomain")
        if type(self.execution_identity) is not ExecutionIdentityBinding:
            raise StudyError("execution_identity must be an exact ExecutionIdentityBinding")
        for name in (
            "task_family",
            "task_payload",
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

        expected_presentation = {
            RepresentationCondition.DIRECT_ANSWER: (
                ComponentTransform.ORIGINAL,
                RelationVisibility.PRESENTED,
                RelationSourceRole.AI,
                False,
            ),
            RepresentationCondition.REPETITION: (
                ComponentTransform.VERBATIM_REPEAT,
                RelationVisibility.WITHHELD,
                RelationSourceRole.UNKNOWN,
                False,
            ),
            RepresentationCondition.RE_REPRESENTATION: (
                ComponentTransform.REORGANIZE_EXISTING,
                RelationVisibility.WITHHELD,
                RelationSourceRole.UNKNOWN,
                False,
            ),
            RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT: (
                ComponentTransform.REORGANIZE_EXISTING,
                RelationVisibility.WITHHELD,
                RelationSourceRole.UNKNOWN,
                True,
            ),
        }[self.condition]
        actual_presentation = (
            self.presentation.component_transform,
            self.presentation.relation_visibility,
            self.presentation.relation_source_role,
            self.presentation.human_judgment_required,
        )
        if actual_presentation != expected_presentation:
            raise StudyError("presentation plan does not match representation condition")

        if self.comparator_role is ComparatorRole.CCTS:
            if self.ccts_manifest_snapshot_sha256 is None:
                raise StudyError("CCTS arm requires admitted manifest snapshot")
            _digest("ccts_manifest_snapshot_sha256", self.ccts_manifest_snapshot_sha256)
            if self.practice_protocol is not None:
                raise StudyError("CCTS arm cannot carry non-CCTS practice protocol")
        else:
            if self.ccts_manifest_snapshot_sha256 is not None:
                raise StudyError("non-CCTS comparator cannot carry a CCTS snapshot")
            if type(self.practice_protocol) is not BoundArtifact:
                raise StudyError("non-CCTS comparator requires a practice protocol artifact")


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
    component_information: tuple[ComponentInformation, ...]
    target_relation_payload: BoundArtifact
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
        if type(self.component_information) is not tuple or not self.component_information or any(
            type(item) is not ComponentInformation for item in self.component_information
        ):
            raise StudyError("component_information must contain exact ComponentInformation values")
        component_ids = [item.component_id for item in self.component_information]
        if len(component_ids) != len(set(component_ids)):
            raise StudyError("component information IDs must be unique")
        component_digests = [item.payload.sha256_digest for item in self.component_information]
        if len(component_digests) != len(set(component_digests)):
            raise StudyError("component information payloads must be content-distinct")
        if type(self.target_relation_payload) is not BoundArtifact:
            raise StudyError("target_relation_payload must be an exact BoundArtifact")
        if self.target_relation_payload.sha256_digest in set(component_digests):
            raise StudyError("target relation payload must remain separate from component information")
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

    components = design.component_information
    component_ids = tuple(item.component_id for item in components)
    component_id_set = set(component_ids)
    component_digests = {item.payload.sha256_digest for item in components}

    arms = design.arms
    if len({arm.arm_id for arm in arms}) != len(arms):
        raise StudyError("contrast arm IDs must be unique")
    ccts_arms = tuple(arm for arm in arms if arm.comparator_role is ComparatorRole.CCTS)
    comparators = tuple(arm for arm in arms if arm.comparator_role is ComparatorRole.NON_CCTS_PRACTICE)
    if len(comparators) != 1 or comparators[0].condition is not (
        RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT
    ):
        raise StudyError("matched non-CCTS practice comparator is required")
    if len(ccts_arms) != 4 or {arm.condition for arm in ccts_arms} != set(RepresentationCondition):
        raise StudyError("exactly four CCTS representation conditions are required")

    comparator = comparators[0]
    practice_protocol = comparator.practice_protocol
    if practice_protocol is None:
        raise StudyError("comparator requires an independent practice protocol")
    if practice_protocol.sha256_digest in component_digests | {design.target_relation_payload.sha256_digest}:
        raise StudyError("practice protocol cannot reuse component or target-relation payload content")
    expected_practice_protocol = render_practice_protocol(
        comparator.presentation,
        comparator.execution_identity,
    )
    if practice_protocol.content_utf8 != expected_practice_protocol:
        raise StudyError("practice protocol must canonically bind the comparator presentation and execution")

    for arm in ccts_arms:
        if arm.ccts_manifest_snapshot_sha256 != snapshot:
            raise StudyError("CCTS arm must bind admitted manifest snapshot")
    for arm in arms:
        if set(arm.presentation.component_ids) != component_id_set or (
            len(arm.presentation.component_ids) != len(component_ids)
        ):
            raise StudyError("presentation must reference exactly the declared component-information set")
        if arm.provenance.sha256_digest != assisted.ccts_manifest.provenance_manifest_sha256:
            raise StudyError("source-role provenance binding drift")
        if arm.task_payload.sha256_digest != assisted.task_payload_sha256:
            raise StudyError("task payload must bind Human agency task")
        if arm.evaluator.sha256_digest != assisted.evaluator_sha256:
            raise StudyError("evaluator binding drift from Human agency audit")
        if arm.rubric.sha256_digest != assisted.scoring_rubric_sha256:
            raise StudyError("rubric binding drift from Human agency audit")

    identities = {item.unit_id: item for item in exposure.execution_identities}
    for arm in arms:
        if identities.get(arm.execution_identity.unit_id) != arm.execution_identity:
            raise StudyError("execution identity must bind the verified task-selection audit")

    base = ccts_arms[0]
    if any(arm.execution_identity != base.execution_identity for arm in ccts_arms[1:]):
        raise StudyError("CCTS representation arms must share one verified execution identity")
    if (
        comparator.execution_identity.unit_id == base.execution_identity.unit_id
        or comparator.execution_identity.execution_id == base.execution_identity.execution_id
    ):
        raise StudyError("non-CCTS comparator requires a distinct verified execution identity")

    matched = (
        ("task_domain", "task domain"),
        ("task_family", "task family"),
        ("task_payload", "task payload"),
        ("exposure_content", "exposure content"),
        ("exposure_intensity", "exposure intensity"),
        ("prior_knowledge", "prior knowledge"),
        ("evaluator", "evaluator"),
        ("rubric", "rubric"),
    )
    for name, label in matched:
        if any(getattr(arm, name) != getattr(base, name) for arm in arms[1:]):
            raise StudyError(f"matched {label} drift")

    units = {unit.unit_id: unit for unit in exposure.units}
    unit = units.get(base.execution_identity.unit_id)
    comparator_unit = units.get(comparator.execution_identity.unit_id)
    if unit is None or comparator_unit is None:
        raise StudyError("execution identity must bind a verified task-selection unit")
    if unit.pair_id != comparator_unit.pair_id:
        raise StudyError("non-CCTS comparator must bind the yoked matched-exposure pair")

    for bound_unit in (unit, comparator_unit):
        if (
            bound_unit.prior_knowledge_control != base.prior_knowledge
            or bound_unit.evaluator_payload != base.evaluator
            or bound_unit.exposure_unit_definition != base.exposure_intensity
        ):
            raise StudyError("task-selection control binding drift")
        if not any(
            event.task_domain is base.task_domain
            and event.task_family_artifact == base.task_family
            and event.exposure_payload_artifact == base.exposure_content
            for event in bound_unit.realized_exposure_trace
        ):
            raise StudyError("exposure content must bind a verified task-domain episode")

    base_signature = tuple(
        (
            event.task_domain,
            event.task_family_artifact.sha256_digest,
            event.exposure_payload_artifact.sha256_digest,
        )
        for event in unit.realized_exposure_trace
    )
    comparator_signature = tuple(
        (
            event.task_domain,
            event.task_family_artifact.sha256_digest,
            event.exposure_payload_artifact.sha256_digest,
        )
        for event in comparator_unit.realized_exposure_trace
    )
    if comparator_signature != base_signature:
        raise StudyError("non-CCTS comparator exposure sequence must match the CCTS execution")

    held_out_digest = design.held_out_task.task_payload_artifact.sha256_digest
    if design.held_out_task.task_domain is not base.task_domain or (
        design.held_out_task.task_family_artifact != base.task_family
    ):
        raise StudyError("held-out task domain/family drift")
    prior_content = (
        {arm.task_payload.sha256_digest for arm in arms}
        | {arm.exposure_content.sha256_digest for arm in arms}
        | component_digests
        | {design.target_relation_payload.sha256_digest}
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
