from __future__ import annotations

from dataclasses import dataclass

from .harness import AdmissionDisposition, StudyError
from .task_selection_exposure import (
    BoundArtifact,
    HeldOutTransferTask,
    SelectionDecision,
    SelectionRegime,
    SelectionTaskDomain,
    TaskSelectionUnit,
)


@dataclass(frozen=True, slots=True)
class ChoiceAlternative:
    task_domain: SelectionTaskDomain
    task_family_artifact: BoundArtifact
    exposure_payload_artifact: BoundArtifact

    def __post_init__(self) -> None:
        if type(self.task_domain) is not SelectionTaskDomain:
            raise StudyError("choice alternative task_domain must be exact SelectionTaskDomain")
        if type(self.task_family_artifact) is not BoundArtifact:
            raise StudyError("choice alternative task_family_artifact must be exact BoundArtifact")
        if type(self.exposure_payload_artifact) is not BoundArtifact:
            raise StudyError("choice alternative exposure_payload_artifact must be exact BoundArtifact")


@dataclass(frozen=True, slots=True)
class ChoiceOpportunity:
    event_index: int
    options: tuple[ChoiceAlternative, ...]
    opportunity_record: BoundArtifact

    def __post_init__(self) -> None:
        if type(self.event_index) is not int or self.event_index < 0:
            raise StudyError("choice opportunity event_index must be a non-negative exact int")
        if type(self.options) is not tuple:
            raise StudyError("choice opportunity options must be an exact tuple")
        if len(self.options) < 2:
            raise StudyError("free choice requires at least two available alternatives")
        if any(type(option) is not ChoiceAlternative for option in self.options):
            raise StudyError("choice opportunity options must contain exact ChoiceAlternative values")
        signatures = tuple(_alternative_signature(option) for option in self.options)
        if len(set(signatures)) != len(signatures):
            raise StudyError("choice opportunity alternatives must be content-distinct")
        if type(self.opportunity_record) is not BoundArtifact:
            raise StudyError("choice opportunity requires an exact BoundArtifact record")


@dataclass(frozen=True, slots=True)
class FreeChoiceOpportunityTrace:
    unit_id: str
    opportunities: tuple[ChoiceOpportunity, ...]

    def __post_init__(self) -> None:
        if type(self.unit_id) is not str or not self.unit_id.strip():
            raise StudyError("choice opportunity trace unit_id must be non-empty text")
        if type(self.opportunities) is not tuple or not self.opportunities:
            raise StudyError("choice opportunity trace requires an exact non-empty tuple")
        if any(type(item) is not ChoiceOpportunity for item in self.opportunities):
            raise StudyError("choice opportunity trace must contain exact ChoiceOpportunity values")
        indices = tuple(item.event_index for item in self.opportunities)
        if indices != tuple(range(len(indices))):
            raise StudyError("choice opportunity event_index values must be contiguous from zero")


@dataclass(frozen=True, slots=True)
class ExecutionIdentityBinding:
    unit_id: str
    execution_id: str
    execution_record_artifact_id: str

    def __post_init__(self) -> None:
        for name in ("unit_id", "execution_id", "execution_record_artifact_id"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise StudyError(f"{name} must be non-empty text")


@dataclass(frozen=True, slots=True)
class HardenedTaskSelectionExposureAudit:
    units: tuple[TaskSelectionUnit, ...]
    choice_opportunity_traces: tuple[FreeChoiceOpportunityTrace, ...]
    execution_identities: tuple[ExecutionIdentityBinding, ...]
    within_family_held_out_tasks: tuple[HeldOutTransferTask, ...]
    cross_family_held_out_tasks: tuple[HeldOutTransferTask, ...]
    complete_design: bool
    pair_count: int
    free_domain_exposure_counts: tuple[tuple[int, ...], ...]
    free_selection_exposure_divergence_observed: bool
    choice_opportunity_sets_bound: bool = True
    chosen_option_membership_verified: bool = True
    execution_identity_separated_from_content: bool = True
    same_content_execution_records_permitted: bool = True
    within_family_payload_holdout_bound: bool = True
    cross_family_domain_generalization_bound: bool = True
    choice_set_temporal_provenance_established: bool = False
    family_level_human_transfer_established: bool = False
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    model_invoked: bool = False
    human_participant_observed: bool = False
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    h_ts1_status: str = "NOT_ESTABLISHED"
    h_dl1_status: str = "NOT_ESTABLISHED"
    h_ra1_status: str = "NOT_TESTED_BY_THIS_HARDENING"
    human_learning: str = "NOT_ESTABLISHED"
    causal_effect: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"


def _alternative_signature(
    option: ChoiceAlternative,
) -> tuple[SelectionTaskDomain, str, str]:
    return (
        option.task_domain,
        option.task_family_artifact.sha256_digest,
        option.exposure_payload_artifact.sha256_digest,
    )


def _decision_signature(
    decision: SelectionDecision,
) -> tuple[SelectionTaskDomain, str, str]:
    return (
        decision.task_domain,
        decision.task_family_sha256,
        decision.exposure_payload_sha256,
    )


def _exposure_signature(
    unit: TaskSelectionUnit,
) -> tuple[tuple[SelectionTaskDomain, str, str], ...]:
    return tuple(
        (
            event.task_domain,
            event.task_family_artifact.sha256_digest,
            event.exposure_payload_artifact.sha256_digest,
        )
        for event in unit.realized_exposure_trace
    )


def _assignment_signature(
    unit: TaskSelectionUnit,
) -> tuple[tuple[SelectionTaskDomain, str, str], ...]:
    return tuple(
        (
            step.task_domain,
            step.task_family_sha256,
            step.exposure_payload_sha256,
        )
        for step in unit.assignment_schedule
    )


def _domain_counts(unit: TaskSelectionUnit) -> tuple[int, ...]:
    return tuple(
        sum(event.task_domain is domain for event in unit.realized_exposure_trace)
        for domain in SelectionTaskDomain
    )


def _index_transfer_tasks(
    tasks: tuple[HeldOutTransferTask, ...],
    label: str,
) -> dict[SelectionTaskDomain, HeldOutTransferTask]:
    if type(tasks) is not tuple or not tasks:
        raise StudyError(f"{label} requires an exact non-empty tuple")
    if any(type(task) is not HeldOutTransferTask for task in tasks):
        raise StudyError(f"{label} must contain exact HeldOutTransferTask values")
    indexed = {task.task_domain: task for task in tasks}
    if set(indexed) != set(SelectionTaskDomain) or len(indexed) != len(tasks):
        raise StudyError(f"{label} requires exactly one task per task domain")
    return indexed


def audit_task_selection_exposure_design_hardened(
    units: tuple[TaskSelectionUnit, ...],
    choice_opportunity_traces: tuple[FreeChoiceOpportunityTrace, ...],
    execution_identities: tuple[ExecutionIdentityBinding, ...],
    within_family_held_out_tasks: tuple[HeldOutTransferTask, ...],
    cross_family_held_out_tasks: tuple[HeldOutTransferTask, ...],
) -> HardenedTaskSelectionExposureAudit:
    if type(units) is not tuple or not units:
        raise StudyError("hardened task-selection design requires units")
    if any(type(unit) is not TaskSelectionUnit for unit in units):
        raise StudyError("units must contain exact TaskSelectionUnit values")

    unit_ids = [unit.unit_id for unit in units]
    if len(unit_ids) != len(set(unit_ids)):
        raise StudyError("unit ids must be unique")

    pairs: dict[str, list[TaskSelectionUnit]] = {}
    for unit in units:
        pairs.setdefault(unit.pair_id, []).append(unit)
    if len(pairs) < 2:
        raise StudyError("hardened design requires at least two anonymous yoked pairs")
    for pair_units in pairs.values():
        if len(pair_units) != 2:
            raise StudyError("each pair_id requires exactly two study units")
        if {unit.selection_regime for unit in pair_units} != set(SelectionRegime):
            raise StudyError("each pair_id requires one free and one yoked-assigned unit")

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
            raise StudyError("each selection regime requires one exact protocol binding")
        protocol_by_regime[regime] = next(iter(digests))
    if len(set(protocol_by_regime.values())) != len(SelectionRegime):
        raise StudyError("selection regimes require content-distinct protocol bindings")

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
        free_signature = _exposure_signature(free)
        if free_signature != _exposure_signature(yoked):
            raise StudyError(f"pair {pair_id} must receive the same realized exposure sequence")
        if _assignment_signature(yoked) != free_signature:
            raise StudyError(f"pair {pair_id} yoked schedule must copy the free unit exposure sequence")

    free_units = tuple(
        unit for unit in units if unit.selection_regime is SelectionRegime.FREE_SELECTION
    )
    free_unit_ids = {unit.unit_id for unit in free_units}
    if type(choice_opportunity_traces) is not tuple or not choice_opportunity_traces:
        raise StudyError("hardened design requires free-choice opportunity traces")
    if any(type(trace) is not FreeChoiceOpportunityTrace for trace in choice_opportunity_traces):
        raise StudyError("choice opportunity traces must contain exact FreeChoiceOpportunityTrace values")
    trace_by_unit = {trace.unit_id: trace for trace in choice_opportunity_traces}
    if len(trace_by_unit) != len(choice_opportunity_traces):
        raise StudyError("each free unit requires exactly one choice opportunity trace")
    if set(trace_by_unit) != free_unit_ids:
        raise StudyError("choice opportunity traces must bind exactly the FREE_SELECTION units")

    for unit in free_units:
        trace = trace_by_unit[unit.unit_id]
        if len(trace.opportunities) != len(unit.realized_choice_trace):
            raise StudyError("choice opportunity count must match realized choice count")
        for decision, opportunity in zip(
            unit.realized_choice_trace,
            trace.opportunities,
            strict=True,
        ):
            if decision.event_index != opportunity.event_index:
                raise StudyError("choice opportunity event_index must match realized choice event_index")
            option_signatures = {_alternative_signature(option) for option in opportunity.options}
            if _decision_signature(decision) not in option_signatures:
                raise StudyError("realized choice must be a member of the bound opportunity set")

    if type(execution_identities) is not tuple or not execution_identities:
        raise StudyError("hardened design requires execution identity bindings")
    if any(type(item) is not ExecutionIdentityBinding for item in execution_identities):
        raise StudyError("execution identities must contain exact ExecutionIdentityBinding values")
    execution_by_unit = {item.unit_id: item for item in execution_identities}
    if len(execution_by_unit) != len(execution_identities):
        raise StudyError("each unit requires exactly one execution identity binding")
    if set(execution_by_unit) != set(unit_ids):
        raise StudyError("execution identity bindings must cover exactly the study units")
    if len({item.execution_id for item in execution_identities}) != len(execution_identities):
        raise StudyError("execution_id values must be unique")
    if len({item.execution_record_artifact_id for item in execution_identities}) != len(
        execution_identities
    ):
        raise StudyError("execution record artifact identities must be unique")
    for unit in units:
        binding = execution_by_unit[unit.unit_id]
        if binding.execution_record_artifact_id != unit.execution_record.artifact_id:
            raise StudyError("execution identity must bind the unit execution_record artifact_id")

    family_by_domain: dict[SelectionTaskDomain, str] = {}
    exposure_payloads: set[str] = set()
    for unit in units:
        for event in unit.realized_exposure_trace:
            family_digest = event.task_family_artifact.sha256_digest
            previous = family_by_domain.setdefault(event.task_domain, family_digest)
            if previous != family_digest:
                raise StudyError("task-family binding drift across exposure units")
            exposure_payloads.add(event.exposure_payload_artifact.sha256_digest)

    within_by_domain = _index_transfer_tasks(
        within_family_held_out_tasks,
        "within-family held-out set",
    )
    cross_by_domain = _index_transfer_tasks(
        cross_family_held_out_tasks,
        "cross-family held-out set",
    )
    evaluator_binding = units[0].evaluator_payload.sha256_digest
    cross_family_digests: set[str] = set()
    all_held_out_payloads: set[str] = set()
    exposed_family_digests = set(family_by_domain.values())

    for domain in SelectionTaskDomain:
        within = within_by_domain[domain]
        cross = cross_by_domain[domain]
        for task in (within, cross):
            if task.evaluator_payload.sha256_digest != evaluator_binding:
                raise StudyError("held-out evaluator binding must match unit evaluator binding")
            payload_digest = task.task_payload_artifact.sha256_digest
            if payload_digest in exposure_payloads:
                raise StudyError("held-out task payload must remain distinct from exposure payloads")
            if payload_digest in all_held_out_payloads:
                raise StudyError("held-out task payloads must be mutually content-distinct")
            all_held_out_payloads.add(payload_digest)

        exposure_family = family_by_domain.get(domain)
        within_family = within.task_family_artifact.sha256_digest
        cross_family = cross.task_family_artifact.sha256_digest
        if exposure_family is not None and within_family != exposure_family:
            raise StudyError("within-family held-out task must match the exposed task family")
        if exposure_family is not None and cross_family == exposure_family:
            raise StudyError("cross-family held-out task must use a family not seen in exposure")
        if exposure_family is None and cross_family == within_family:
            raise StudyError("zero-exposure domains still require two distinct held-out families")
        if cross_family in exposed_family_digests:
            raise StudyError("cross-family held-out family must be globally absent from exposure")
        if cross_family in cross_family_digests:
            raise StudyError("cross-family held-out family bindings must be unique by domain")
        cross_family_digests.add(cross_family)

    free_counts = tuple(_domain_counts(unit) for unit in free_units)
    divergence = len(set(free_counts)) > 1

    return HardenedTaskSelectionExposureAudit(
        units=units,
        choice_opportunity_traces=choice_opportunity_traces,
        execution_identities=execution_identities,
        within_family_held_out_tasks=within_family_held_out_tasks,
        cross_family_held_out_tasks=cross_family_held_out_tasks,
        complete_design=True,
        pair_count=len(pairs),
        free_domain_exposure_counts=free_counts,
        free_selection_exposure_divergence_observed=divergence,
    )
