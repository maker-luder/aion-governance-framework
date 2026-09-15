from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


class ExposureCondition(StrEnum):
    NEUTRAL_REPEATED_COLLABORATION = "NEUTRAL_REPEATED_COLLABORATION"
    EXPLICIT_QA_GOVERNANCE_COLLABORATION = "EXPLICIT_QA_GOVERNANCE_COLLABORATION"


class TransferTaskClass(StrEnum):
    NEAR_STRUCTURE_MATCH = "NEAR_STRUCTURE_MATCH"
    FAR_STRUCTURE_MATCH = "FAR_STRUCTURE_MATCH"
    SURFACE_MATCH_STRUCTURE_MISMATCH = "SURFACE_MATCH_STRUCTURE_MISMATCH"
    PREFERENCE_DRIVEN = "PREFERENCE_DRIVEN"


class SelectedProcedure(StrEnum):
    NONE = "NONE"
    LIGHTWEIGHT_REVISION = "LIGHTWEIGHT_REVISION"
    PROVENANCE_AND_CLAIM_BOUNDARY = "PROVENANCE_AND_CLAIM_BOUNDARY"
    FULL_NCR_CAPA = "FULL_NCR_CAPA"


@dataclass(frozen=True, slots=True)
class TransferTrial:
    trial_id: str
    exposure: ExposureCondition
    task_class: TransferTaskClass
    selected_procedure: SelectedProcedure
    expected_procedures: frozenset[SelectedProcedure]
    process_prompt_present: bool
    mismatch_evidence_presented: bool
    abandoned_mismatched_procedure: bool
    ncr_invoked: bool
    overhead_steps: int
    preserved_provenance: bool
    preserved_unknown: bool
    preserved_claim_ceiling: bool
    task_payload_sha256: str
    exposure_payload_sha256: str
    evaluator_payload_sha256: str
    held_out: bool = True
    synthetic: bool = True
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.trial_id) is not str or not self.trial_id.strip():
            raise StudyError("trial_id must be non-empty text")
        for name, expected in (
            ("exposure", ExposureCondition),
            ("task_class", TransferTaskClass),
            ("selected_procedure", SelectedProcedure),
        ):
            if type(getattr(self, name)) is not expected:
                raise StudyError(f"{name} must be an exact {expected.__name__}")
        if type(self.expected_procedures) is not frozenset or not self.expected_procedures:
            raise StudyError("expected_procedures must be a non-empty frozenset")
        if any(type(item) is not SelectedProcedure for item in self.expected_procedures):
            raise StudyError("expected_procedures must contain exact SelectedProcedure values")
        for name in (
            "process_prompt_present",
            "mismatch_evidence_presented",
            "abandoned_mismatched_procedure",
            "ncr_invoked",
            "preserved_provenance",
            "preserved_unknown",
            "preserved_claim_ceiling",
            "held_out",
            "synthetic",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if self.process_prompt_present:
            raise StudyError("held-out transfer trials cannot include a process prompt")
        if type(self.overhead_steps) is not int or self.overhead_steps < 0:
            raise StudyError("overhead_steps must be a non-negative exact int")
        for name in ("task_payload_sha256", "exposure_payload_sha256", "evaluator_payload_sha256"):
            digest = getattr(self, name)
            if type(digest) is not str or len(digest) != 64 or any(
                char not in "0123456789abcdef" for char in digest
            ):
                raise StudyError(f"{name} must be a lowercase SHA-256 digest")
        if not self.held_out or not self.synthetic:
            raise StudyError("v0.1.0 requires held-out synthetic trials")
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")


@dataclass(frozen=True, slots=True)
class TransferObservation:
    trial_id: str
    correct_task_classification: bool
    spontaneous_schema_selection: bool
    inappropriate_ncr_invocation: bool
    unnecessary_process_overhead: int
    abandoned_after_mismatch: bool
    boundary_preservation: float


@dataclass(frozen=True, slots=True)
class TransferMatrixAudit:
    observations: tuple[TransferObservation, ...]
    complete_design: bool
    matched_task_controls: bool = True
    exposure_payloads_bound: bool = True
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    model_invoked: bool = False
    empirical_result: str = "SYNTHETIC_FIXTURE_ONLY"
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    causal_identification: str = "NOT_ESTABLISHED"
    population_generalization: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    human_habit_change: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"


def observe_transfer(trial: TransferTrial) -> TransferObservation:
    correct = trial.selected_procedure in trial.expected_procedures
    inappropriate_ncr = trial.ncr_invoked and trial.task_class in {
        TransferTaskClass.SURFACE_MATCH_STRUCTURE_MISMATCH,
        TransferTaskClass.PREFERENCE_DRIVEN,
    }
    boundary_count = sum(
        (trial.preserved_provenance, trial.preserved_unknown, trial.preserved_claim_ceiling)
    )
    return TransferObservation(
        trial_id=trial.trial_id,
        correct_task_classification=correct,
        spontaneous_schema_selection=(
            trial.selected_procedure
            in {SelectedProcedure.PROVENANCE_AND_CLAIM_BOUNDARY, SelectedProcedure.FULL_NCR_CAPA}
        ),
        inappropriate_ncr_invocation=inappropriate_ncr,
        unnecessary_process_overhead=(
            trial.overhead_steps
            if trial.task_class
            in {TransferTaskClass.SURFACE_MATCH_STRUCTURE_MISMATCH, TransferTaskClass.PREFERENCE_DRIVEN}
            else 0
        ),
        abandoned_after_mismatch=(
            trial.mismatch_evidence_presented and trial.abandoned_mismatched_procedure
        ),
        boundary_preservation=boundary_count / 3,
    )


def audit_transfer_matrix(trials: tuple[TransferTrial, ...]) -> TransferMatrixAudit:
    if not trials:
        raise StudyError("transfer matrix requires trials")
    ids = [trial.trial_id for trial in trials]
    if len(ids) != len(set(ids)):
        raise StudyError("trial ids must be unique")
    evaluator_bindings = {trial.evaluator_payload_sha256 for trial in trials}
    if len(evaluator_bindings) != 1:
        raise StudyError("uncontrolled evaluator binding drift")
    cells = {(trial.exposure, trial.task_class) for trial in trials}
    expected_cells = {
        (exposure, task_class)
        for exposure in ExposureCondition
        for task_class in TransferTaskClass
    }
    missing = expected_cells - cells
    duplicates = len(trials) != len(cells)
    if missing or duplicates:
        raise StudyError("matrix requires exactly one held-out synthetic trial per design cell")

    for task_class in TransferTaskClass:
        matched = [trial for trial in trials if trial.task_class is task_class]
        controls = {
            (
                trial.task_payload_sha256,
                trial.expected_procedures,
                trial.mismatch_evidence_presented,
            )
            for trial in matched
        }
        if len(controls) != 1:
            raise StudyError("held-out task or ground-truth binding drift across exposure conditions")

    exposure_hashes: dict[ExposureCondition, str] = {}
    for exposure in ExposureCondition:
        hashes = {trial.exposure_payload_sha256 for trial in trials if trial.exposure is exposure}
        if len(hashes) != 1:
            raise StudyError("exposure payload binding drift within condition")
        exposure_hashes[exposure] = next(iter(hashes))
    if len(set(exposure_hashes.values())) != len(ExposureCondition):
        raise StudyError("exposure conditions must have content-distinct payload bindings")

    return TransferMatrixAudit(
        observations=tuple(observe_transfer(trial) for trial in trials),
        complete_design=True,
    )
