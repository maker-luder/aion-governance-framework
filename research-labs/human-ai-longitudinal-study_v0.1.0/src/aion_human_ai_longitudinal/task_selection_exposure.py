from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib

from .harness import AdmissionDisposition, StudyError


class SelectionRegime(StrEnum):
    FREE_SELECTION = "FREE_SELECTION"
    YOKED_ASSIGNED_EXPOSURE = "YOKED_ASSIGNED_EXPOSURE"


class SelectionTaskDomain(StrEnum):
    IMAGE_VISUAL = "IMAGE_VISUAL"
    CREATIVE_TEXT = "CREATIVE_TEXT"
    RESEARCH_PROVENANCE = "RESEARCH_PROVENANCE"
    GIT_ENGINEERING = "GIT_ENGINEERING"


class ExposureUnitKind(StrEnum):
    TASK_EPISODE = "TASK_EPISODE"


@dataclass(frozen=True, slots=True)
class BoundArtifact:
    artifact_id: str
    content_utf8: str
    sha256_digest: str

    def __post_init__(self) -> None:
        if type(self.artifact_id) is not str or not self.artifact_id.strip():
            raise StudyError("artifact_id must be non-empty text")
        if type(self.content_utf8) is not str or not self.content_utf8:
            raise StudyError("content_utf8 must be non-empty text")
        _validate_sha256(self.sha256_digest, "sha256_digest")
        computed = hashlib.sha256(self.content_utf8.encode("utf-8")).hexdigest()
        if computed != self.sha256_digest:
            raise StudyError("sha256_digest must match content_utf8")


@dataclass(frozen=True, slots=True)
class SelectionDecision:
    event_index: int
    task_domain: SelectionTaskDomain
    task_family_sha256: str
    exposure_payload_sha256: str

    def __post_init__(self) -> None:
        _validate_event_index(self.event_index)
        _validate_exact_domain(self.task_domain)
        _validate_sha256(self.task_family_sha256, "task_family_sha256")
        _validate_sha256(self.exposure_payload_sha256, "exposure_payload_sha256")


@dataclass(frozen=True, slots=True)
class AssignmentStep:
    event_index: int
    task_domain: SelectionTaskDomain
    task_family_sha256: str
    exposure_payload_sha256: str

    def __post_init__(self) -> None:
        _validate_event_index(self.event_index)
        _validate_exact_domain(self.task_domain)
        _validate_sha256(self.task_family_sha256, "task_family_sha256")
        _validate_sha256(self.exposure_payload_sha256, "exposure_payload_sha256")


@dataclass(frozen=True, slots=True)
class ExposureEvent:
    event_index: int
    task_domain: SelectionTaskDomain
    task_family_artifact: BoundArtifact
    exposure_payload_artifact: BoundArtifact

    def __post_init__(self) -> None:
        _validate_event_index(self.event_index)
        _validate_exact_domain(self.task_domain)
        if type(self.task_family_artifact) is not BoundArtifact:
            raise StudyError("task_family_artifact must be an exact BoundArtifact")
        if type(self.exposure_payload_artifact) is not BoundArtifact:
            raise StudyError("exposure_payload_artifact must be an exact BoundArtifact")


@dataclass(frozen=True, slots=True)
class TaskSelectionUnit:
    unit_id: str
    pair_id: str
    selection_regime: SelectionRegime
    selection_protocol: BoundArtifact
    realized_choice_trace: tuple[SelectionDecision, ...]
    assignment_schedule: tuple[AssignmentStep, ...]
    realized_exposure_trace: tuple[ExposureEvent, ...]
    execution_record: BoundArtifact
    exposure_unit_kind: ExposureUnitKind
    exposure_unit_definition: BoundArtifact
    access_profile: BoundArtifact
    model_configuration: BoundArtifact
    tool_access: BoundArtifact
    evaluator_payload: BoundArtifact
    prior_knowledge_control: BoundArtifact
    time_budget_control: BoundArtifact
    task_difficulty_control: BoundArtifact
    resource_cost_information: BoundArtifact
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        for name in ("unit_id", "pair_id"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise StudyError(f"{name} must be non-empty text")
        if type(self.selection_regime) is not SelectionRegime:
            raise StudyError("selection_regime must be an exact SelectionRegime")
        if type(self.selection_protocol) is not BoundArtifact:
            raise StudyError("selection_protocol must be an exact BoundArtifact")
        if type(self.exposure_unit_kind) is not ExposureUnitKind:
            raise StudyError("exposure_unit_kind must be an exact ExposureUnitKind")
        for name in (
            "exposure_unit_definition",
            "execution_record",
            "access_profile",
            "model_configuration",
            "tool_access",
            "evaluator_payload",
            "prior_knowledge_control",
            "time_budget_control",
            "task_difficulty_control",
            "resource_cost_information",
        ):
            if type(getattr(self, name)) is not BoundArtifact:
                raise StudyError(f"{name} must be an exact BoundArtifact")
        for name in (
            "realized_choice_trace",
            "assignment_schedule",
            "realized_exposure_trace",
        ):
            if type(getattr(self, name)) is not tuple:
                raise StudyError(f"{name} must be an exact tuple")
        if not self.realized_exposure_trace:
            raise StudyError("realized_exposure_trace must contain at least one task episode")
        if any(type(item) is not ExposureEvent for item in self.realized_exposure_trace):
            raise StudyError("realized_exposure_trace must contain exact ExposureEvent values")
        _require_contiguous_indices(
            tuple(event.event_index for event in self.realized_exposure_trace),
            "realized_exposure_trace",
        )
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
            raise StudyError("v0.1.0 requires synthetic task-selection units")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "v0.1.0 is structural QA only and cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")

        if self.selection_regime is SelectionRegime.FREE_SELECTION:
            if self.assignment_schedule:
                raise StudyError("FREE_SELECTION units cannot contain an assignment_schedule")
            if not self.realized_choice_trace:
                raise StudyError("FREE_SELECTION units require a realized_choice_trace")
            if any(
                type(item) is not SelectionDecision for item in self.realized_choice_trace
            ):
                raise StudyError(
                    "realized_choice_trace must contain exact SelectionDecision values"
                )
            _require_contiguous_indices(
                tuple(item.event_index for item in self.realized_choice_trace),
                "realized_choice_trace",
            )
            if _decision_signature(self.realized_choice_trace) != _exposure_signature(
                self.realized_exposure_trace
            ):
                raise StudyError(
                    "free-selection realized choices must bind the realized exposure trace"
                )
        else:
            if self.realized_choice_trace:
                raise StudyError(
                    "YOKED_ASSIGNED_EXPOSURE units cannot claim a realized_choice_trace"
                )
            if not self.assignment_schedule:
                raise StudyError(
                    "YOKED_ASSIGNED_EXPOSURE units require an assignment_schedule"
                )
            if any(type(item) is not AssignmentStep for item in self.assignment_schedule):
                raise StudyError(
                    "assignment_schedule must contain exact AssignmentStep values"
                )
            _require_contiguous_indices(
                tuple(item.event_index for item in self.assignment_schedule),
                "assignment_schedule",
            )
            if _assignment_signature(self.assignment_schedule) != _exposure_signature(
                self.realized_exposure_trace
            ):
                raise StudyError(
                    "assigned schedule must bind the assigned unit's realized exposure trace"
                )


@dataclass(frozen=True, slots=True)
class HeldOutTransferTask:
    task_domain: SelectionTaskDomain
    task_family_artifact: BoundArtifact
    task_payload_artifact: BoundArtifact
    evaluator_payload: BoundArtifact
    held_out: bool = True
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _validate_exact_domain(self.task_domain)
        for name in (
            "task_family_artifact",
            "task_payload_artifact",
            "evaluator_payload",
        ):
            if type(getattr(self, name)) is not BoundArtifact:
                raise StudyError(f"{name} must be an exact BoundArtifact")
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
            raise StudyError(
                "v0.1.0 is structural QA only and cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")


@dataclass(frozen=True, slots=True)
class TaskSelectionExposureAudit:
    units: tuple[TaskSelectionUnit, ...]
    held_out_tasks: tuple[HeldOutTransferTask, ...]
    complete_design: bool
    pair_count: int
    free_domain_exposure_counts: tuple[tuple[int, ...], ...]
    free_selection_exposure_divergence_observed: bool
    true_yoked_pairing: bool = True
    free_selection_null_permitted: bool = True
    protocol_schedule_choice_exposure_separated: bool = True
    zero_domain_exposure_permitted: bool = True
    exposure_unit_definition_bound: bool = True
    content_hash_verified: bool = True
    separate_execution_records: bool = True
    same_access_controls: bool = True
    task_family_controls: bool = True
    held_out_payload_separation: bool = True
    resource_cost_information_controlled: bool = True
    design_unit: str = "BETWEEN_UNIT_YOKED_PAIR"
    exposure_unit: str = "TASK_EPISODE_EVENT_COUNT"
    cross_domain_commensurability: str = "EVENT_COUNT_ONLY_NOT_INTENSITY"
    temporal_provenance_status: str = "SPECIFICATION_BOUND_NOT_EMPIRICALLY_POPULATED"
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


def _validate_event_index(value: int) -> None:
    if type(value) is not int or value < 0:
        raise StudyError("event_index must be a non-negative exact int")


def _validate_exact_domain(value: SelectionTaskDomain) -> None:
    if type(value) is not SelectionTaskDomain:
        raise StudyError("task_domain must be an exact SelectionTaskDomain")


def _require_contiguous_indices(indices: tuple[int, ...], name: str) -> None:
    if indices != tuple(range(len(indices))):
        raise StudyError(f"{name} event_index values must be contiguous from zero")


def _exposure_signature(
    events: tuple[ExposureEvent, ...],
) -> tuple[tuple[SelectionTaskDomain, str, str], ...]:
    return tuple(
        (
            event.task_domain,
            event.task_family_artifact.sha256_digest,
            event.exposure_payload_artifact.sha256_digest,
        )
        for event in events
    )


def _decision_signature(
    decisions: tuple[SelectionDecision, ...],
) -> tuple[tuple[SelectionTaskDomain, str, str], ...]:
    return tuple(
        (item.task_domain, item.task_family_sha256, item.exposure_payload_sha256)
        for item in decisions
    )


def _assignment_signature(
    steps: tuple[AssignmentStep, ...],
) -> tuple[tuple[SelectionTaskDomain, str, str], ...]:
    return tuple(
        (item.task_domain, item.task_family_sha256, item.exposure_payload_sha256)
        for item in steps
    )


def _domain_counts(unit: TaskSelectionUnit) -> tuple[int, ...]:
    return tuple(
        sum(event.task_domain is domain for event in unit.realized_exposure_trace)
        for domain in SelectionTaskDomain
    )


def audit_task_selection_exposure_design(
    units: tuple[TaskSelectionUnit, ...],
    held_out_tasks: tuple[HeldOutTransferTask, ...],
) -> TaskSelectionExposureAudit:
    if type(units) is not tuple or not units:
        raise StudyError("task-selection design requires units")
    if type(held_out_tasks) is not tuple or not held_out_tasks:
        raise StudyError("task-selection design requires held-out transfer tasks")
    if any(type(unit) is not TaskSelectionUnit for unit in units):
        raise StudyError("units must contain exact TaskSelectionUnit values")
    if any(type(task) is not HeldOutTransferTask for task in held_out_tasks):
        raise StudyError(
            "held_out_tasks must contain exact HeldOutTransferTask values"
        )

    unit_ids = [unit.unit_id for unit in units]
    if len(unit_ids) != len(set(unit_ids)):
        raise StudyError("unit ids must be unique")

    pairs: dict[str, list[TaskSelectionUnit]] = {}
    for unit in units:
        pairs.setdefault(unit.pair_id, []).append(unit)
    if len(pairs) < 2:
        raise StudyError("design requires at least two anonymous yoked pairs")
    for pair_units in pairs.values():
        if len(pair_units) != 2:
            raise StudyError("each pair_id requires exactly two study units")
        regimes = {unit.selection_regime for unit in pair_units}
        if regimes != set(SelectionRegime):
            raise StudyError(
                "each pair_id requires one free and one yoked-assigned unit"
            )

    control_fields = (
        "exposure_unit_definition",
        "access_profile",
        "model_configuration",
        "tool_access",
        "evaluator_payload",
        "prior_knowledge_control",
        "time_budget_control",
        "task_difficulty_control",
        "resource_cost_information",
    )
    for field in control_fields:
        if len({getattr(unit, field).sha256_digest for unit in units}) != 1:
            raise StudyError(f"uncontrolled {field} drift")

    protocol_by_regime: dict[SelectionRegime, str] = {}
    for regime in SelectionRegime:
        digests = {
            unit.selection_protocol.sha256_digest
            for unit in units
            if unit.selection_regime is regime
        }
        if len(digests) != 1:
            raise StudyError(
                "each selection regime requires one exact protocol binding"
            )
        protocol_by_regime[regime] = next(iter(digests))
    if len(set(protocol_by_regime.values())) != len(SelectionRegime):
        raise StudyError(
            "selection regimes require content-distinct protocol bindings"
        )

    execution_digests = {unit.execution_record.sha256_digest for unit in units}
    if len(execution_digests) != len(units):
        raise StudyError("each study unit requires a distinct execution record")

    for pair_id, pair_units in pairs.items():
        free = next(
            unit
            for unit in pair_units
            if unit.selection_regime is SelectionRegime.FREE_SELECTION
        )
        yoked = next(
            unit
            for unit in pair_units
            if unit.selection_regime is SelectionRegime.YOKED_ASSIGNED_EXPOSURE
        )
        free_signature = _exposure_signature(free.realized_exposure_trace)
        yoked_signature = _exposure_signature(yoked.realized_exposure_trace)
        if free_signature != yoked_signature:
            raise StudyError(
                f"pair {pair_id} must receive the same realized exposure sequence"
            )
        if _assignment_signature(yoked.assignment_schedule) != free_signature:
            raise StudyError(
                f"pair {pair_id} yoked schedule must copy the free unit exposure sequence"
            )

    family_by_domain: dict[SelectionTaskDomain, str] = {}
    exposure_payloads: set[str] = set()
    for unit in units:
        for event in unit.realized_exposure_trace:
            digest = event.task_family_artifact.sha256_digest
            previous = family_by_domain.setdefault(event.task_domain, digest)
            if previous != digest:
                raise StudyError("task-family binding drift across units")
            exposure_payloads.add(event.exposure_payload_artifact.sha256_digest)

    transfer_by_domain = {task.task_domain: task for task in held_out_tasks}
    if set(transfer_by_domain) != set(SelectionTaskDomain) or len(
        transfer_by_domain
    ) != len(held_out_tasks):
        raise StudyError(
            "held-out transfer set requires exactly one task per task domain"
        )
    evaluator_binding = units[0].evaluator_payload.sha256_digest
    for domain, task in transfer_by_domain.items():
        if task.evaluator_payload.sha256_digest != evaluator_binding:
            raise StudyError(
                "held-out evaluator binding must match unit evaluator binding"
            )
        family_digest = family_by_domain.get(domain)
        if (
            family_digest is not None
            and task.task_family_artifact.sha256_digest != family_digest
        ):
            raise StudyError(
                "held-out task-family binding must match exposure task family"
            )
        if task.task_payload_artifact.sha256_digest in exposure_payloads:
            raise StudyError(
                "held-out task payload must remain distinct from exposure payloads"
            )

    free_units = tuple(
        unit for unit in units if unit.selection_regime is SelectionRegime.FREE_SELECTION
    )
    free_counts = tuple(_domain_counts(unit) for unit in free_units)
    divergence = len(set(free_counts)) > 1

    return TaskSelectionExposureAudit(
        units=units,
        held_out_tasks=held_out_tasks,
        complete_design=True,
        pair_count=len(pairs),
        free_domain_exposure_counts=free_counts,
        free_selection_exposure_divergence_observed=divergence,
    )