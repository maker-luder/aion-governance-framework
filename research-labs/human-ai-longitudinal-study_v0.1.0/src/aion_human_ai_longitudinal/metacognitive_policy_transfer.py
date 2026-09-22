from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    audit_co_constructed_thinking_space,
)
from .ccts_epistemic_revision import ContentAddressedText
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
    HUMAN_JUDGMENT_AUDIT = "HUMAN_JUDGMENT_AUDIT"
    AI_WITHHELD_HELD_OUT_TRANSFER = "AI_WITHHELD_HELD_OUT_TRANSFER"


class HumanJudgmentDecision(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    UNKNOWN = "UNKNOWN"


class HeldOutTransferScope(StrEnum):
    WITHIN_FAMILY_NEW_PAYLOAD = "WITHIN_FAMILY_NEW_PAYLOAD"
    CROSS_FAMILY_SAME_DOMAIN = "CROSS_FAMILY_SAME_DOMAIN"


@dataclass(frozen=True, slots=True)
class EpistemicAgencyControlManifest:
    task_difficulty: ContentAddressedText
    domain_familiarity: ContentAddressedText
    prior_exposure: ContentAddressedText
    allowed_resources: ContentAddressedText
    time_budget: ContentAddressedText
    evaluator_blinding: ContentAddressedText
    practice_exposure: ContentAddressedText
    demand_characteristics: ContentAddressedText
    system_instructions: ContentAddressedText
    memory_personalization_repository_access: ContentAddressedText
    provider_model_version: ContentAddressedText
    information_quantity: ContentAddressedText
    policy_vocabulary_exposure: ContentAddressedText

    def __post_init__(self) -> None:
        for name in (
            "task_difficulty",
            "domain_familiarity",
            "prior_exposure",
            "allowed_resources",
            "time_budget",
            "evaluator_blinding",
            "practice_exposure",
            "demand_characteristics",
            "system_instructions",
            "memory_personalization_repository_access",
            "provider_model_version",
            "information_quantity",
            "policy_vocabulary_exposure",
        ):
            if type(getattr(self, name)) is not ContentAddressedText:
                raise StudyError(f"{name} must be exact ContentAddressedText")

    def matched_signature(self) -> tuple[str, ...]:
        return (
            self.task_difficulty.sha256_hex,
            self.domain_familiarity.sha256_hex,
            self.prior_exposure.sha256_hex,
            self.allowed_resources.sha256_hex,
            self.time_budget.sha256_hex,
            self.evaluator_blinding.sha256_hex,
            self.practice_exposure.sha256_hex,
            self.demand_characteristics.sha256_hex,
        )

    def access_signature(self) -> tuple[str, ...]:
        return (
            self.system_instructions.sha256_hex,
            self.memory_personalization_repository_access.sha256_hex,
            self.provider_model_version.sha256_hex,
            self.information_quantity.sha256_hex,
            self.policy_vocabulary_exposure.sha256_hex,
        )


@dataclass(frozen=True, slots=True)
class EpistemicAgencyLeakageCheck:
    check_completed: bool
    answer_key_exposed: bool
    held_out_payload_exposed_before_phase: bool
    equivalent_answer_exposure_detected: bool
    policy_text_exposed_when_withheld: bool
    prior_policy_vocabulary_overlap_detected: bool

    def __post_init__(self) -> None:
        for name in (
            "check_completed",
            "answer_key_exposed",
            "held_out_payload_exposed_before_phase",
            "equivalent_answer_exposure_detected",
            "policy_text_exposed_when_withheld",
            "prior_policy_vocabulary_overlap_detected",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.check_completed:
            raise StudyError("leakage check must be completed")
        if (
            self.answer_key_exposed
            or self.held_out_payload_exposed_before_phase
            or self.equivalent_answer_exposure_detected
            or self.policy_text_exposed_when_withheld
        ):
            raise StudyError("answer/policy leakage invalidates the structural trial")


@dataclass(frozen=True, slots=True)
class HumanEpistemicAgencyTrial:
    trial_id: str
    unit_id: str
    condition: HumanEpistemicAgencyCondition
    phase_index: int
    task_class: MetacognitiveTaskClass
    task_family: ContentAddressedText
    task_payload: ContentAddressedText
    condition_manifest: ContentAddressedText
    human_output: ContentAddressedText
    evaluator: ContentAddressedText
    scoring_rubric: ContentAddressedText
    controls: EpistemicAgencyControlManifest
    leakage_check: EpistemicAgencyLeakageCheck
    policy_access: PolicyAccessCondition
    held_out_scope: HeldOutTransferScope | None
    ccts_manifest: CoConstructedThinkingSpaceManifest | None
    decision: HumanJudgmentDecision | None = None
    rationale: ContentAddressedText | None = None
    ai_proposal: ContentAddressedText | None = None
    ai_proposal_contribution_id: str | None = None
    held_out: bool = False
    ai_assistance_available: bool = False
    ccts_scaffold_available: bool = False
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
        if type(self.condition) is not HumanEpistemicAgencyCondition:
            raise StudyError("condition must be an exact HumanEpistemicAgencyCondition")
        if type(self.phase_index) is not int:
            raise StudyError("phase_index must be an exact int")
        if type(self.task_class) is not MetacognitiveTaskClass:
            raise StudyError("task_class must be an exact MetacognitiveTaskClass")
        for name in (
            "task_family",
            "task_payload",
            "condition_manifest",
            "human_output",
            "evaluator",
            "scoring_rubric",
        ):
            if type(getattr(self, name)) is not ContentAddressedText:
                raise StudyError(f"{name} must be exact ContentAddressedText")
        if type(self.controls) is not EpistemicAgencyControlManifest:
            raise StudyError("controls must be exact EpistemicAgencyControlManifest")
        if type(self.leakage_check) is not EpistemicAgencyLeakageCheck:
            raise StudyError("leakage_check must be exact EpistemicAgencyLeakageCheck")
        if type(self.policy_access) is not PolicyAccessCondition:
            raise StudyError("policy_access must be an exact PolicyAccessCondition")
        if self.held_out_scope is not None and type(self.held_out_scope) is not HeldOutTransferScope:
            raise StudyError("held_out_scope must be an exact HeldOutTransferScope or None")
        if self.decision is not None and type(self.decision) is not HumanJudgmentDecision:
            raise StudyError("decision must be an exact HumanJudgmentDecision or None")
        for name in ("rationale", "ai_proposal"):
            value = getattr(self, name)
            if value is not None and type(value) is not ContentAddressedText:
                raise StudyError(f"{name} must be ContentAddressedText or None")
        if (
            self.ai_proposal_contribution_id is not None
            and (
                type(self.ai_proposal_contribution_id) is not str
                or not self.ai_proposal_contribution_id.strip()
            )
        ):
            raise StudyError("ai_proposal_contribution_id must be non-empty text or None")
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

        expected = {
            HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE: (
                0,
                False,
                False,
                False,
                PolicyAccessCondition.POLICY_WITHHELD,
            ),
            HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE: (
                1,
                False,
                True,
                True,
                PolicyAccessCondition.POLICY_AVAILABLE,
            ),
            HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT: (
                2,
                False,
                False,
                False,
                PolicyAccessCondition.POLICY_AVAILABLE,
            ),
            HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER: (
                3,
                True,
                False,
                False,
                PolicyAccessCondition.POLICY_WITHHELD,
            ),
        }
        expected_phase, expected_held_out, expected_ai, expected_ccts, expected_policy = expected[
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
        if self.policy_access is not expected_policy:
            raise StudyError(
                "policy_access does not match the declared epistemic-agency condition"
            )

        if self.condition is HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER:
            if type(self.held_out_scope) is not HeldOutTransferScope:
                raise StudyError("held-out transfer requires an exact transfer scope")
        elif self.held_out_scope is not None:
            raise StudyError("non-held-out conditions cannot declare held_out_scope")

        ccts_bound_conditions = {
            HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE,
            HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT,
        }
        if self.condition in ccts_bound_conditions:
            if type(self.ccts_manifest) is not CoConstructedThinkingSpaceManifest:
                raise StudyError(
                    "CCTS and judgment-audit conditions require an exact CCTS manifest"
                )
            audit_co_constructed_thinking_space(self.ccts_manifest)
            if self.ccts_manifest.problem_representation_sha256 != self.task_payload.sha256_hex:
                raise StudyError("CCTS manifest must bind the trial task payload")
        elif self.ccts_manifest is not None:
            raise StudyError("AI-withheld conditions cannot carry a CCTS manifest")

        if self.condition is HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT:
            if self.decision is None or self.rationale is None or self.ai_proposal is None:
                raise StudyError(
                    "judgment audit requires decision, rationale, and AI proposal"
                )
            if self.ai_proposal_contribution_id is None:
                raise StudyError(
                    "judgment audit requires ai_proposal_contribution_id"
                )
            role_by_id = {
                item.contribution_id: item.role
                for item in self.ccts_manifest.contributions
            }
            payload_by_id = {
                item.contribution_id: item.payload_sha256
                for item in self.ccts_manifest.contributions
            }
            if self.ai_proposal_contribution_id not in role_by_id:
                raise StudyError("AI proposal contribution must resolve in CCTS manifest")
            if (
                role_by_id[self.ai_proposal_contribution_id]
                is not ContributionRole.AI_COLLABORATOR
            ):
                raise StudyError("AI proposal contribution must have AI_COLLABORATOR role")
            if (
                payload_by_id[self.ai_proposal_contribution_id]
                != self.ai_proposal.sha256_hex
            ):
                raise StudyError(
                    "AI proposal content must resolve to the declared CCTS contribution"
                )
        elif (
            self.decision is not None
            or self.rationale is not None
            or self.ai_proposal is not None
            or self.ai_proposal_contribution_id is not None
        ):
            raise StudyError(
                "proposal decision/rationale fields belong only to HUMAN_JUDGMENT_AUDIT"
            )


@dataclass(frozen=True, slots=True)
class HumanEpistemicAgencyObservation:
    trial_id: str
    condition: HumanEpistemicAgencyCondition
    decision: HumanJudgmentDecision | None
    proposal_bound: bool
    rationale_bound: bool
    active_ai_assistance_withheld: bool
    ai_information_withheld: bool
    judgment_of_ai_proposal_candidate: bool
    independent_judgment_candidate: bool
    held_out_scope: HeldOutTransferScope | None
    policy_vocabulary_overlap_detected: bool


@dataclass(frozen=True, slots=True)
class HumanEpistemicAgencyAudit:
    observations: tuple[HumanEpistemicAgencyObservation, ...]
    complete_design: bool
    same_unit_trajectory_bound: bool = True
    trajectory_order_bound: bool = True
    judgment_audit_phase_bound: bool = True
    proposal_decision_rationale_bound: bool = True
    ccts_contract_bound: bool = True
    verified_content_addressing: bool = True
    matched_baseline_ccts_audit_tasks: bool = True
    within_family_held_out_bound: bool = True
    cross_family_held_out_bound: bool = True
    matched_controls_bound: bool = True
    policy_access_bound: bool = True
    leakage_checks_passed: bool = True
    rubric_bound: bool = True
    evaluator_bound: bool = True
    condition_isolation: bool = True
    vocabulary_overlap_flag_count: int = 0
    global_agency_score_computed: bool = False
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    model_invoked: bool = False
    human_participant_observed: bool = False
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    preserved_human_judgment: str = "NOT_SCIENTIFICALLY_ESTABLISHED"
    independent_transfer: str = "NOT_ESTABLISHED"
    cross_family_transfer: str = "NOT_ESTABLISHED"
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
    active_ai_assistance_withheld = not trial.ai_assistance_available
    ai_information_withheld = trial.condition in {
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
        HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
    }
    judgment_audit = (
        trial.condition is HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT
    )
    held_out = (
        trial.condition
        is HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
    )
    return HumanEpistemicAgencyObservation(
        trial_id=trial.trial_id,
        condition=trial.condition,
        decision=trial.decision,
        proposal_bound=judgment_audit and trial.ai_proposal is not None,
        rationale_bound=judgment_audit and trial.rationale is not None,
        active_ai_assistance_withheld=active_ai_assistance_withheld,
        ai_information_withheld=ai_information_withheld,
        judgment_of_ai_proposal_candidate=judgment_audit,
        independent_judgment_candidate=held_out and ai_information_withheld,
        held_out_scope=trial.held_out_scope,
        policy_vocabulary_overlap_detected=(
            trial.leakage_check.prior_policy_vocabulary_overlap_detected
        ),
    )


def audit_human_epistemic_agency_matrix(
    trials: tuple[HumanEpistemicAgencyTrial, ...],
) -> HumanEpistemicAgencyAudit:
    if type(trials) is not tuple or not trials:
        raise StudyError("human epistemic-agency matrix requires a non-empty tuple")
    if any(type(trial) is not HumanEpistemicAgencyTrial for trial in trials):
        raise StudyError(
            "human epistemic-agency matrix requires exact HumanEpistemicAgencyTrial values"
        )

    ids = [trial.trial_id for trial in trials]
    if len(ids) != len(set(ids)):
        raise StudyError("trial ids must be unique")

    unit_ids = {trial.unit_id for trial in trials}
    if len(unit_ids) != 1:
        raise StudyError(
            "retention matrix requires one anonymous study unit across conditions"
        )

    evaluators = {trial.evaluator.sha256_hex for trial in trials}
    if len(evaluators) != 1:
        raise StudyError("uncontrolled evaluator binding drift")
    rubrics = {trial.scoring_rubric.sha256_hex for trial in trials}
    if len(rubrics) != 1:
        raise StudyError("uncontrolled scoring-rubric binding drift")

    expected_per_task = {
        (
            HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
            None,
        ),
        (
            HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE,
            None,
        ),
        (
            HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT,
            None,
        ),
        (
            HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
            HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD,
        ),
        (
            HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
            HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN,
        ),
    }
    cells = {
        (trial.task_class, trial.condition, trial.held_out_scope)
        for trial in trials
    }
    expected_cells = {
        (task_class, condition, scope)
        for task_class in MetacognitiveTaskClass
        for condition, scope in expected_per_task
    }
    if cells != expected_cells or len(trials) != len(cells):
        raise StudyError(
            "matrix requires baseline, CCTS, judgment audit, and both held-out scopes per task class"
        )

    condition_bindings: dict[tuple[HumanEpistemicAgencyCondition, HeldOutTransferScope | None], str] = {}
    for condition, scope in expected_per_task:
        hashes = {
            trial.condition_manifest.sha256_hex
            for trial in trials
            if trial.condition is condition and trial.held_out_scope is scope
        }
        if len(hashes) != 1:
            raise StudyError("condition manifest binding drift")
        condition_bindings[(condition, scope)] = next(iter(hashes))
    if len(set(condition_bindings.values())) != len(condition_bindings):
        raise StudyError("condition/scope manifests must be content-distinct")

    access_signatures: dict[
        tuple[HumanEpistemicAgencyCondition, HeldOutTransferScope | None],
        tuple[str, ...],
    ] = {}
    for condition, scope in expected_per_task:
        signatures = {
            trial.controls.access_signature()
            for trial in trials
            if trial.condition is condition and trial.held_out_scope is scope
        }
        if len(signatures) != 1:
            raise StudyError("condition access-control binding drift")
        access_signatures[(condition, scope)] = next(iter(signatures))

    for task_class in MetacognitiveTaskClass:
        task_trials = [trial for trial in trials if trial.task_class is task_class]
        matched_signatures = {
            trial.controls.matched_signature() for trial in task_trials
        }
        if len(matched_signatures) != 1:
            raise StudyError("matched-control manifest drift")

        by_key = {
            (trial.condition, trial.held_out_scope): trial for trial in task_trials
        }
        baseline = by_key[
            (HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE, None)
        ]
        ccts = by_key[(HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE, None)]
        judgment = by_key[
            (HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT, None)
        ]
        within = by_key[
            (
                HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
                HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD,
            )
        ]
        cross = by_key[
            (
                HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
                HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN,
            )
        ]

        if not (
            baseline.task_family.sha256_hex
            == ccts.task_family.sha256_hex
            == judgment.task_family.sha256_hex
            == within.task_family.sha256_hex
        ):
            raise StudyError(
                "baseline, CCTS, judgment audit, and within-family transfer require one task family"
            )
        if cross.task_family.sha256_hex == baseline.task_family.sha256_hex:
            raise StudyError("cross-family held-out transfer requires a distinct task family")
        if not (
            baseline.task_payload.sha256_hex
            == ccts.task_payload.sha256_hex
            == judgment.task_payload.sha256_hex
        ):
            raise StudyError(
                "baseline, CCTS, and judgment audit require matched task payloads"
            )
        if within.task_payload.sha256_hex == baseline.task_payload.sha256_hex:
            raise StudyError("within-family held-out transfer requires a distinct task payload")
        if cross.task_payload.sha256_hex in {
            baseline.task_payload.sha256_hex,
            within.task_payload.sha256_hex,
        }:
            raise StudyError(
                "cross-family held-out transfer requires a content-distinct task payload"
            )
        if ccts.ccts_manifest is None or judgment.ccts_manifest is None:
            raise StudyError(
                "CCTS and judgment-audit matrix cells require CCTS manifests"
            )
        if ccts.ccts_manifest.space_id != judgment.ccts_manifest.space_id:
            raise StudyError(
                "judgment audit must bind the same CCTS space as the assisted condition"
            )

    observations = tuple(
        observe_human_epistemic_agency(trial) for trial in trials
    )
    return HumanEpistemicAgencyAudit(
        observations=observations,
        complete_design=True,
        vocabulary_overlap_flag_count=sum(
            item.policy_vocabulary_overlap_detected for item in observations
        ),
    )
