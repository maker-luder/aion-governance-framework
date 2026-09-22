from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    audit_co_constructed_thinking_space,
)
from .harness import AdmissionDisposition, StudyError


class PolicyExposureCondition(StrEnum):
    EXTERNALIZED_METACOGNITIVE_POLICY = "EXTERNALIZED_METACOGNITIVE_POLICY"
    CONTENT_MATCHED_NON_POLICY_EXPOSURE = "CONTENT_MATCHED_NON_POLICY_EXPOSURE"


class PolicyAccessCondition(StrEnum):
    POLICY_AVAILABLE = "POLICY_AVAILABLE"
    POLICY_WITHHELD = "POLICY_WITHHELD"


class MetacognitiveTaskClass(StrEnum):
    SOURCE_ROLE_CONFLICT = "SOURCE_ROLE_CONFLICT"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    COMPREHENSION_THRESHOLD = "COMPREHENSION_THRESHOLD"
    HYPOTHESIS_STRESS_TEST = "HYPOTHESIS_STRESS_TEST"
    LOW_STAKES_NEGATIVE_CONTROL = "LOW_STAKES_NEGATIVE_CONTROL"


class MetacognitiveAction(StrEnum):
    CHECK_SOURCE_ROLE = "CHECK_SOURCE_ROLE"
    PRESERVE_UNKNOWN = "PRESERVE_UNKNOWN"
    VERIFY_COMPREHENSION = "VERIFY_COMPREHENSION"
    ADAPT_EXPLANATION_GRANULARITY = "ADAPT_EXPLANATION_GRANULARITY"
    SEARCH_COUNTEREVIDENCE = "SEARCH_COUNTEREVIDENCE"
    DISTINGUISH_OBSERVATION_INFERENCE = "DISTINGUISH_OBSERVATION_INFERENCE"
    LIGHTWEIGHT_RESPONSE = "LIGHTWEIGHT_RESPONSE"


@dataclass(frozen=True, slots=True)
class MetacognitiveTransferTrial:
    trial_id: str
    exposure: PolicyExposureCondition
    policy_access: PolicyAccessCondition
    task_class: MetacognitiveTaskClass
    expected_actions: frozenset[MetacognitiveAction]
    observed_actions: frozenset[MetacognitiveAction]
    explicit_process_prompt_present: bool
    task_family_sha256: str
    task_payload_sha256: str
    exposure_content_family_sha256: str
    exposure_payload_sha256: str
    access_payload_sha256: str
    evaluator_payload_sha256: str
    held_out: bool = True
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.trial_id) is not str or not self.trial_id.strip():
            raise StudyError("trial_id must be non-empty text")
        for name, expected in (
            ("exposure", PolicyExposureCondition),
            ("policy_access", PolicyAccessCondition),
            ("task_class", MetacognitiveTaskClass),
        ):
            if type(getattr(self, name)) is not expected:
                raise StudyError(f"{name} must be an exact {expected.__name__}")
        for name in ("expected_actions", "observed_actions"):
            actions = getattr(self, name)
            if type(actions) is not frozenset or not actions:
                raise StudyError(f"{name} must be a non-empty frozenset")
            if any(type(action) is not MetacognitiveAction for action in actions):
                raise StudyError(f"{name} must contain exact MetacognitiveAction values")
        for name in (
            "explicit_process_prompt_present",
            "held_out",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if self.explicit_process_prompt_present:
            raise StudyError("transfer trials cannot include an explicit process prompt")
        if not self.held_out or not self.synthetic:
            raise StudyError("v0.1.0 requires held-out synthetic trials")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError("v0.1.0 is structural QA only and cannot contain model or human observations")
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")
        for name in (
            "task_family_sha256",
            "task_payload_sha256",
            "exposure_content_family_sha256",
            "exposure_payload_sha256",
            "access_payload_sha256",
            "evaluator_payload_sha256",
        ):
            digest = getattr(self, name)
            if type(digest) is not str or len(digest) != 64 or any(
                char not in "0123456789abcdef" for char in digest
            ):
                raise StudyError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class MetacognitiveTransferObservation:
    trial_id: str
    exact_action_match: bool
    missing_actions: tuple[MetacognitiveAction, ...]
    unexpected_actions: tuple[MetacognitiveAction, ...]
    scaffolded_policy_application_candidate: bool
    independent_transfer_candidate: bool
    overprocessing_negative_control: bool


@dataclass(frozen=True, slots=True)
class MetacognitiveTransferAudit:
    observations: tuple[MetacognitiveTransferObservation, ...]
    complete_design: bool
    matched_task_controls: bool = True
    matched_exposure_content: bool = True
    distinct_exposure_bindings: bool = True
    distinct_access_bindings: bool = True
    held_out_payload_separation: bool = True
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    model_invoked: bool = False
    human_participant_observed: bool = False
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    causal_effect: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    independent_transfer: str = "NOT_ESTABLISHED"
    metacognitive_internalization: str = "NOT_ESTABLISHED"
    dependency_effect: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"


def observe_metacognitive_transfer(
    trial: MetacognitiveTransferTrial,
) -> MetacognitiveTransferObservation:
    missing = tuple(sorted(trial.expected_actions - trial.observed_actions, key=str))
    unexpected = tuple(sorted(trial.observed_actions - trial.expected_actions, key=str))
    exact = not missing and not unexpected
    externalized = trial.exposure is PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY
    available = trial.policy_access is PolicyAccessCondition.POLICY_AVAILABLE
    negative_control = trial.task_class is MetacognitiveTaskClass.LOW_STAKES_NEGATIVE_CONTROL
    return MetacognitiveTransferObservation(
        trial_id=trial.trial_id,
        exact_action_match=exact,
        missing_actions=missing,
        unexpected_actions=unexpected,
        scaffolded_policy_application_candidate=(externalized and available and exact),
        independent_transfer_candidate=(externalized and not available and exact),
        overprocessing_negative_control=(negative_control and bool(unexpected)),
    )


def audit_metacognitive_transfer_matrix(
    trials: tuple[MetacognitiveTransferTrial, ...],
) -> MetacognitiveTransferAudit:
    if not trials:
        raise StudyError("metacognitive transfer matrix requires trials")

    ids = [trial.trial_id for trial in trials]
    if len(ids) != len(set(ids)):
        raise StudyError("trial ids must be unique")

    cells = {
        (trial.exposure, trial.policy_access, trial.task_class)
        for trial in trials
    }
    expected_cells = {
        (exposure, access, task_class)
        for exposure in PolicyExposureCondition
        for access in PolicyAccessCondition
        for task_class in MetacognitiveTaskClass
    }
    if cells != expected_cells or len(trials) != len(cells):
        raise StudyError("matrix requires exactly one held-out synthetic trial per design cell")

    evaluator_bindings = {trial.evaluator_payload_sha256 for trial in trials}
    if len(evaluator_bindings) != 1:
        raise StudyError("uncontrolled evaluator binding drift")

    exposure_content_families = {
        trial.exposure_content_family_sha256 for trial in trials
    }
    if len(exposure_content_families) != 1:
        raise StudyError("exposure content-family binding drift")

    for task_class in MetacognitiveTaskClass:
        task_trials = [trial for trial in trials if trial.task_class is task_class]
        families = {trial.task_family_sha256 for trial in task_trials}
        expected_actions = {trial.expected_actions for trial in task_trials}
        if len(families) != 1 or len(expected_actions) != 1:
            raise StudyError("task family or expected-action binding drift")

        by_access: dict[PolicyAccessCondition, set[str]] = {
            access: {
                trial.task_payload_sha256
                for trial in task_trials
                if trial.policy_access is access
            }
            for access in PolicyAccessCondition
        }
        if any(len(payloads) != 1 for payloads in by_access.values()):
            raise StudyError("task payload must be matched across exposure conditions")
        if len({next(iter(payloads)) for payloads in by_access.values()}) != len(
            PolicyAccessCondition
        ):
            raise StudyError("policy-available and policy-withheld phases require distinct held-out payloads")

    exposure_hashes: dict[PolicyExposureCondition, str] = {}
    for exposure in PolicyExposureCondition:
        hashes = {
            trial.exposure_payload_sha256
            for trial in trials
            if trial.exposure is exposure
        }
        if len(hashes) != 1:
            raise StudyError("exposure payload binding drift within condition")
        exposure_hashes[exposure] = next(iter(hashes))
    if len(set(exposure_hashes.values())) != len(PolicyExposureCondition):
        raise StudyError("exposure conditions must have content-distinct payload bindings")

    access_hashes: dict[PolicyAccessCondition, str] = {}
    for access in PolicyAccessCondition:
        hashes = {
            trial.access_payload_sha256
            for trial in trials
            if trial.policy_access is access
        }
        if len(hashes) != 1:
            raise StudyError("policy-access payload binding drift within condition")
        access_hashes[access] = next(iter(hashes))
    if len(set(access_hashes.values())) != len(PolicyAccessCondition):
        raise StudyError("policy access conditions must have content-distinct payload bindings")

    return MetacognitiveTransferAudit(
        observations=tuple(observe_metacognitive_transfer(trial) for trial in trials),
        complete_design=True,
    )


class HumanEpistemicAgencyCondition(StrEnum):
    AI_WITHHELD_BASELINE = "AI_WITHHELD_BASELINE"
    CCTS_AI_AVAILABLE = "CCTS_AI_AVAILABLE"
    AI_WITHHELD_HELD_OUT_TRANSFER = "AI_WITHHELD_HELD_OUT_TRANSFER"


class HumanJudgmentDecision(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class HumanEpistemicAgencyTrial:
    trial_id: str
    unit_id: str
    condition: HumanEpistemicAgencyCondition
    phase_index: int
    task_class: MetacognitiveTaskClass
    decision: HumanJudgmentDecision
    rationale_text: str
    rationale_sha256: str
    task_family_sha256: str
    task_payload_sha256: str
    condition_payload_sha256: str
    evaluator_payload_sha256: str
    ccts_manifest: CoConstructedThinkingSpaceManifest | None
    held_out: bool
    ai_assistance_available: bool
    ccts_scaffold_available: bool
    explicit_process_prompt_present: bool = False
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.trial_id) is not str or not self.trial_id.strip():
            raise StudyError("trial_id must be non-empty text")
        if type(self.unit_id) is not str or not self.unit_id.strip():
            raise StudyError("unit_id must be non-empty text")
        if type(self.rationale_text) is not str or not self.rationale_text.strip():
            raise StudyError("rationale_text must be non-empty text")
        if type(self.condition) is not HumanEpistemicAgencyCondition:
            raise StudyError("condition must be an exact HumanEpistemicAgencyCondition")
        if type(self.phase_index) is not int:
            raise StudyError("phase_index must be an exact int")
        if type(self.task_class) is not MetacognitiveTaskClass:
            raise StudyError("task_class must be an exact MetacognitiveTaskClass")
        if type(self.decision) is not HumanJudgmentDecision:
            raise StudyError("decision must be an exact HumanJudgmentDecision")
        for name in (
            "held_out",
            "ai_assistance_available",
            "ccts_scaffold_available",
            "explicit_process_prompt_present",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic:
            raise StudyError("v0.1.0 accepts synthetic trials only")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "v0.1.0 is structural QA only and cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")
        if self.explicit_process_prompt_present:
            raise StudyError(
                "human judgment audit cannot be forced by an explicit process prompt"
            )
        expected_flags = {
            HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE: (0, False, False, False),
            HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE: (1, False, True, True),
            HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER: (
                2,
                True,
                False,
                False,
            ),
        }
        expected_phase, expected_held_out, expected_ai, expected_ccts = expected_flags[
            self.condition
        ]
        if self.phase_index != expected_phase:
            raise StudyError(
                "phase_index does not match the declared epistemic-agency condition"
            )
        if (
            self.held_out is not expected_held_out
            or self.ai_assistance_available is not expected_ai
            or self.ccts_scaffold_available is not expected_ccts
        ):
            raise StudyError(
                "condition flags do not match the declared epistemic-agency condition"
            )
        if self.condition is HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE:
            if type(self.ccts_manifest) is not CoConstructedThinkingSpaceManifest:
                raise StudyError(
                    "CCTS condition requires an exact CoConstructedThinkingSpaceManifest"
                )
            audit_co_constructed_thinking_space(self.ccts_manifest)
            if self.ccts_manifest.problem_representation_sha256 != self.task_payload_sha256:
                raise StudyError("CCTS manifest must bind the trial task payload")
        elif self.ccts_manifest is not None:
            raise StudyError("AI-withheld conditions cannot carry a CCTS manifest")
        for name in (
            "rationale_sha256",
            "task_family_sha256",
            "task_payload_sha256",
            "condition_payload_sha256",
            "evaluator_payload_sha256",
        ):
            digest = getattr(self, name)
            if type(digest) is not str or len(digest) != 64 or any(
                char not in "0123456789abcdef" for char in digest
            ):
                raise StudyError(f"{name} must be a lowercase SHA-256 digest")
        if sha256(self.rationale_text.encode("utf-8")).hexdigest() != self.rationale_sha256:
            raise StudyError("rationale_sha256 must match rationale_text")


@dataclass(frozen=True, slots=True)
class HumanEpistemicAgencyObservation:
    trial_id: str
    condition: HumanEpistemicAgencyCondition
    decision: HumanJudgmentDecision
    rationale_bound: bool
    ai_withheld: bool
    independent_judgment_candidate: bool


@dataclass(frozen=True, slots=True)
class HumanEpistemicAgencyAudit:
    observations: tuple[HumanEpistemicAgencyObservation, ...]
    complete_design: bool
    same_unit_trajectory_bound: bool = True
    trajectory_order_bound: bool = True
    ccts_contract_bound: bool = True
    verified_rationale_content_addressing: bool = True
    matched_baseline_ccts_tasks: bool = True
    held_out_payload_separation: bool = True
    condition_isolation: bool = True
    rationale_binding_complete: bool = True
    global_agency_score_computed: bool = False
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    model_invoked: bool = False
    human_participant_observed: bool = False
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    preserved_human_judgment: str = "NOT_SCIENTIFICALLY_ESTABLISHED"
    independent_transfer: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    dependency_effect: str = "NOT_ESTABLISHED"
    causal_effect: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"


def observe_human_epistemic_agency(
    trial: HumanEpistemicAgencyTrial,
) -> HumanEpistemicAgencyObservation:
    ai_withheld = not trial.ai_assistance_available
    return HumanEpistemicAgencyObservation(
        trial_id=trial.trial_id,
        condition=trial.condition,
        decision=trial.decision,
        rationale_bound=True,
        ai_withheld=ai_withheld,
        independent_judgment_candidate=(
            trial.condition
            is HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
            and ai_withheld
        ),
    )


def audit_human_epistemic_agency_matrix(
    trials: tuple[HumanEpistemicAgencyTrial, ...],
) -> HumanEpistemicAgencyAudit:
    if not trials:
        raise StudyError("human epistemic-agency matrix requires trials")

    ids = [trial.trial_id for trial in trials]
    if len(ids) != len(set(ids)):
        raise StudyError("trial ids must be unique")

    cells = {(trial.condition, trial.task_class) for trial in trials}
    expected_cells = {
        (condition, task_class)
        for condition in HumanEpistemicAgencyCondition
        for task_class in MetacognitiveTaskClass
    }
    if cells != expected_cells or len(trials) != len(cells):
        raise StudyError(
            "matrix requires exactly one synthetic trial per condition and task class"
        )

    unit_ids = {trial.unit_id for trial in trials}
    if len(unit_ids) != 1:
        raise StudyError(
            "retention matrix requires one anonymous study unit across conditions"
        )

    evaluator_bindings = {trial.evaluator_payload_sha256 for trial in trials}
    if len(evaluator_bindings) != 1:
        raise StudyError("uncontrolled evaluator binding drift")

    condition_bindings: dict[HumanEpistemicAgencyCondition, str] = {}
    for condition in HumanEpistemicAgencyCondition:
        hashes = {
            trial.condition_payload_sha256
            for trial in trials
            if trial.condition is condition
        }
        if len(hashes) != 1:
            raise StudyError("condition payload binding drift within condition")
        condition_bindings[condition] = next(iter(hashes))
    if len(set(condition_bindings.values())) != len(HumanEpistemicAgencyCondition):
        raise StudyError(
            "epistemic-agency conditions require distinct payload bindings"
        )

    for task_class in MetacognitiveTaskClass:
        task_trials = [
            trial for trial in trials if trial.task_class is task_class
        ]
        families = {trial.task_family_sha256 for trial in task_trials}
        if len(families) != 1:
            raise StudyError("task family binding drift")

        by_condition = {
            trial.condition: trial.task_payload_sha256 for trial in task_trials
        }
        if (
            by_condition[HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE]
            != by_condition[HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE]
        ):
            raise StudyError(
                "baseline and CCTS conditions require matched task payloads"
            )
        if (
            by_condition[
                HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
            ]
            == by_condition[HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE]
        ):
            raise StudyError("held-out transfer requires a distinct task payload")

    return HumanEpistemicAgencyAudit(
        observations=tuple(
            observe_human_epistemic_agency(trial) for trial in trials
        ),
        complete_design=True,
    )
