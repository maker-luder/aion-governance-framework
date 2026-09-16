from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


class SelectionRegime(StrEnum):
    FREE_SELECTION = "FREE_SELECTION"
    MATCHED_ASSIGNED_EXPOSURE = "MATCHED_ASSIGNED_EXPOSURE"


class SyntheticTrack(StrEnum):
    TRACK_A = "TRACK_A"
    TRACK_B = "TRACK_B"


class SelectionTaskDomain(StrEnum):
    IMAGE_VISUAL = "IMAGE_VISUAL"
    CREATIVE_TEXT = "CREATIVE_TEXT"
    RESEARCH_PROVENANCE = "RESEARCH_PROVENANCE"
    GIT_ENGINEERING = "GIT_ENGINEERING"


@dataclass(frozen=True, slots=True)
class DomainExposure:
    task_domain: SelectionTaskDomain
    exposure_units: int
    task_family_sha256: str
    exposure_payload_sha256: str

    def __post_init__(self) -> None:
        if type(self.task_domain) is not SelectionTaskDomain:
            raise StudyError("task_domain must be an exact SelectionTaskDomain")
        if type(self.exposure_units) is not int or self.exposure_units <= 0:
            raise StudyError("exposure_units must be a positive exact int")
        _validate_sha256(self.task_family_sha256, "task_family_sha256")
        _validate_sha256(self.exposure_payload_sha256, "exposure_payload_sha256")


@dataclass(frozen=True, slots=True)
class TaskSelectionArm:
    arm_id: str
    selection_regime: SelectionRegime
    synthetic_track: SyntheticTrack
    exposures: tuple[DomainExposure, ...]
    selection_protocol_sha256: str
    selection_trace_sha256: str
    access_profile_sha256: str
    model_configuration_sha256: str
    tool_access_sha256: str
    evaluator_payload_sha256: str
    prior_knowledge_control_sha256: str
    time_budget_sha256: str
    task_difficulty_control_sha256: str
    resource_cost_information_sha256: str
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.arm_id) is not str or not self.arm_id.strip():
            raise StudyError("arm_id must be non-empty text")
        if type(self.selection_regime) is not SelectionRegime:
            raise StudyError("selection_regime must be an exact SelectionRegime")
        if type(self.synthetic_track) is not SyntheticTrack:
            raise StudyError("synthetic_track must be an exact SyntheticTrack")
        if type(self.exposures) is not tuple or not self.exposures:
            raise StudyError("exposures must be a non-empty tuple")
        if any(type(item) is not DomainExposure for item in self.exposures):
            raise StudyError("exposures must contain exact DomainExposure values")
        for name in (
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic:
            raise StudyError("v0.1.0 requires synthetic task-selection arms")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError("v0.1.0 is structural QA only and cannot contain model or human observations")
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")
        for name in (
            "selection_protocol_sha256",
            "selection_trace_sha256",
            "access_profile_sha256",
            "model_configuration_sha256",
            "tool_access_sha256",
            "evaluator_payload_sha256",
            "prior_knowledge_control_sha256",
            "time_budget_sha256",
            "task_difficulty_control_sha256",
            "resource_cost_information_sha256",
        ):
            _validate_sha256(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class HeldOutTransferTask:
    task_domain: SelectionTaskDomain
    task_family_sha256: str
    task_payload_sha256: str
    evaluator_payload_sha256: str
    held_out: bool = True
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.task_domain) is not SelectionTaskDomain:
            raise StudyError("task_domain must be an exact SelectionTaskDomain")
        for name in (
            "held_out",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.held_out or not self.synthetic:
            raise StudyError("v0.1.0 requires held-out synthetic transfer tasks")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError("v0.1.0 is structural QA only and cannot contain model or human observations")
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")
        _validate_sha256(self.task_family_sha256, "task_family_sha256")
        _validate_sha256(self.task_payload_sha256, "task_payload_sha256")
        _validate_sha256(self.evaluator_payload_sha256, "evaluator_payload_sha256")


@dataclass(frozen=True, slots=True)
class TaskSelectionExposureAudit:
    arms: tuple[TaskSelectionArm, ...]
    held_out_tasks: tuple[HeldOutTransferTask, ...]
    complete_design: bool
    same_access_controls: bool = True
    selection_protocol_bound: bool = True
    selection_trace_bound: bool = True
    matched_assigned_exposure: bool = True
    free_selection_exposure_divergence: bool = True
    matched_total_exposure: bool = True
    task_family_controls: bool = True
    held_out_payload_separation: bool = True
    resource_cost_information_controlled: bool = True
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    model_invoked: bool = False
    human_participant_observed: bool = False
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    h_ts1_status: str = "NOT_ESTABLISHED"
    h_dl1_status: str = "NOT_ESTABLISHED"
    h_ra1_status: str = "NOT_TESTED_BY_THIS_HARNESS"
    human_learning: str = "NOT_ESTABLISHED"
    causal_effect: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"


def _validate_sha256(value: str, name: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _domain_map(arm: TaskSelectionArm) -> dict[SelectionTaskDomain, DomainExposure]:
    result = {exposure.task_domain: exposure for exposure in arm.exposures}
    if set(result) != set(SelectionTaskDomain) or len(result) != len(arm.exposures):
        raise StudyError("each arm requires exactly one exposure record per task domain")
    return result


def _exposure_vector(arm: TaskSelectionArm) -> tuple[int, ...]:
    exposures = _domain_map(arm)
    return tuple(exposures[domain].exposure_units for domain in SelectionTaskDomain)


def audit_task_selection_exposure_design(
    arms: tuple[TaskSelectionArm, ...],
    held_out_tasks: tuple[HeldOutTransferTask, ...],
) -> TaskSelectionExposureAudit:
    if not arms:
        raise StudyError("task-selection design requires arms")
    if not held_out_tasks:
        raise StudyError("task-selection design requires held-out transfer tasks")

    arm_ids = [arm.arm_id for arm in arms]
    if len(arm_ids) != len(set(arm_ids)):
        raise StudyError("arm ids must be unique")

    cells = {(arm.selection_regime, arm.synthetic_track) for arm in arms}
    expected_cells = {
        (regime, track)
        for regime in SelectionRegime
        for track in SyntheticTrack
    }
    if cells != expected_cells or len(arms) != len(cells):
        raise StudyError("design requires exactly one arm per regime and synthetic track")

    control_fields = (
        "access_profile_sha256",
        "model_configuration_sha256",
        "tool_access_sha256",
        "evaluator_payload_sha256",
        "prior_knowledge_control_sha256",
        "time_budget_sha256",
        "task_difficulty_control_sha256",
        "resource_cost_information_sha256",
    )
    for field in control_fields:
        if len({getattr(arm, field) for arm in arms}) != 1:
            raise StudyError(f"uncontrolled {field} drift")

    protocol_by_regime: dict[SelectionRegime, str] = {}
    for regime in SelectionRegime:
        regime_protocols = {
            arm.selection_protocol_sha256
            for arm in arms
            if arm.selection_regime is regime
        }
        if len(regime_protocols) != 1:
            raise StudyError("each selection regime requires one exact protocol binding")
        protocol_by_regime[regime] = next(iter(regime_protocols))
    if len(set(protocol_by_regime.values())) != len(SelectionRegime):
        raise StudyError("selection regimes require content-distinct protocol bindings")

    domain_maps = {arm.arm_id: _domain_map(arm) for arm in arms}
    for domain in SelectionTaskDomain:
        task_families = {
            domain_maps[arm.arm_id][domain].task_family_sha256
            for arm in arms
        }
        if len(task_families) != 1:
            raise StudyError("task-family binding drift across arms")

    totals = {sum(_exposure_vector(arm)) for arm in arms}
    if len(totals) != 1:
        raise StudyError("total exposure must be matched across arms")

    assigned = {
        arm.synthetic_track: arm
        for arm in arms
        if arm.selection_regime is SelectionRegime.MATCHED_ASSIGNED_EXPOSURE
    }
    if _exposure_vector(assigned[SyntheticTrack.TRACK_A]) != _exposure_vector(
        assigned[SyntheticTrack.TRACK_B]
    ):
        raise StudyError("matched assigned-exposure tracks require identical exposure distributions")
    if assigned[SyntheticTrack.TRACK_A].selection_trace_sha256 != assigned[
        SyntheticTrack.TRACK_B
    ].selection_trace_sha256:
        raise StudyError("matched assigned-exposure tracks require one exact assignment trace")
    for domain in SelectionTaskDomain:
        left = domain_maps[assigned[SyntheticTrack.TRACK_A].arm_id][domain]
        right = domain_maps[assigned[SyntheticTrack.TRACK_B].arm_id][domain]
        if left.exposure_payload_sha256 != right.exposure_payload_sha256:
            raise StudyError("matched assigned-exposure tracks require identical exposure payloads")

    free = {
        arm.synthetic_track: arm
        for arm in arms
        if arm.selection_regime is SelectionRegime.FREE_SELECTION
    }
    free_a = _exposure_vector(free[SyntheticTrack.TRACK_A])
    free_b = _exposure_vector(free[SyntheticTrack.TRACK_B])
    if free_a == free_b:
        raise StudyError("free-selection tracks must encode different effective exposure distributions")
    if free[SyntheticTrack.TRACK_A].selection_trace_sha256 == free[
        SyntheticTrack.TRACK_B
    ].selection_trace_sha256:
        raise StudyError("free-selection tracks require content-distinct synthetic selection traces")

    transfer_by_domain = {task.task_domain: task for task in held_out_tasks}
    if set(transfer_by_domain) != set(SelectionTaskDomain) or len(transfer_by_domain) != len(
        held_out_tasks
    ):
        raise StudyError("held-out transfer set requires exactly one task per task domain")

    evaluator_binding = arms[0].evaluator_payload_sha256
    exposure_payloads = {
        exposure.exposure_payload_sha256
        for arm in arms
        for exposure in arm.exposures
    }
    for domain, transfer in transfer_by_domain.items():
        if transfer.evaluator_payload_sha256 != evaluator_binding:
            raise StudyError("held-out evaluator binding must match arm evaluator binding")
        family = domain_maps[arms[0].arm_id][domain].task_family_sha256
        if transfer.task_family_sha256 != family:
            raise StudyError("held-out task-family binding must match exposure task family")
        if transfer.task_payload_sha256 in exposure_payloads:
            raise StudyError("held-out task payload must remain distinct from exposure payloads")

    return TaskSelectionExposureAudit(
        arms=arms,
        held_out_tasks=held_out_tasks,
        complete_design=True,
    )
