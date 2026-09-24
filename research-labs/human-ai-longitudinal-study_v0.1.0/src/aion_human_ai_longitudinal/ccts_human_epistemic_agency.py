from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from hashlib import sha256
import json

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    audit_co_constructed_thinking_space,
)
from .harness import AdmissionDisposition, StudyError
from .metacognitive_policy_transfer import (
    MetacognitiveTaskClass,
    PolicyAccessCondition,
)


class HumanAgencyCondition(StrEnum):
    AI_WITHHELD_BASELINE = "AI_WITHHELD_BASELINE"
    CCTS_AI_AVAILABLE = "CCTS_AI_AVAILABLE"
    AI_WITHHELD_JUDGMENT = "AI_WITHHELD_JUDGMENT"
    AI_WITHHELD_HELD_OUT = "AI_WITHHELD_HELD_OUT"


class HumanJudgmentDisposition(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    MODIFY = "MODIFY"
    UNKNOWN = "UNKNOWN"


class HeldOutTransferScope(StrEnum):
    WITHIN_FAMILY_NEW_PAYLOAD = "WITHIN_FAMILY_NEW_PAYLOAD"
    CROSS_FAMILY_SAME_DOMAIN = "CROSS_FAMILY_SAME_DOMAIN"


def _validate_digest(name: str, digest: str) -> None:
    if type(digest) is not str or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _validate_git_head(name: str, head: str) -> None:
    if type(head) is not str or len(head) != 40 or any(
        char not in "0123456789abcdef" for char in head
    ):
        raise StudyError(f"{name} must be a lowercase 40-character Git SHA")


def _validate_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def ccts_manifest_snapshot_sha256(
    manifest: CoConstructedThinkingSpaceManifest,
) -> str:
    if type(manifest) is not CoConstructedThinkingSpaceManifest:
        raise StudyError(
            "manifest must be an exact CoConstructedThinkingSpaceManifest"
        )
    audit_co_constructed_thinking_space(manifest)
    canonical = json.dumps(
        asdict(manifest),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class HumanAgencyControlManifest:
    task_difficulty_sha256: str
    domain_familiarity_sha256: str
    allowed_resources_sha256: str
    time_budget_sha256: str
    evaluator_blinding_sha256: str
    practice_exposure_sha256: str

    def __post_init__(self) -> None:
        for name in (
            "task_difficulty_sha256",
            "domain_familiarity_sha256",
            "allowed_resources_sha256",
            "time_budget_sha256",
            "evaluator_blinding_sha256",
            "practice_exposure_sha256",
        ):
            _validate_digest(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class ValidationHeadBinding:
    implementation_head: str
    validation_head: str
    historical_pass_receipt: bool

    def __post_init__(self) -> None:
        _validate_git_head("implementation_head", self.implementation_head)
        _validate_git_head("validation_head", self.validation_head)
        if type(self.historical_pass_receipt) is not bool:
            raise StudyError("historical_pass_receipt must be an exact bool")
        if self.historical_pass_receipt and (
            self.implementation_head != self.validation_head
        ):
            raise StudyError("historical PASS cannot validate changed code")


@dataclass(frozen=True, slots=True)
class CCTSHumanAgencyTrial:
    trial_id: str
    unit_id: str
    condition: HumanAgencyCondition
    phase_index: int
    task_class: MetacognitiveTaskClass
    task_domain_sha256: str
    task_family_sha256: str
    task_payload_sha256: str
    human_output_sha256: str
    evaluator_sha256: str
    scoring_rubric_sha256: str
    controls: HumanAgencyControlManifest
    condition_manifest_sha256: str
    source_role: ContributionRole
    source_role_provenance_sha256: str
    policy_access: PolicyAccessCondition
    judgment: HumanJudgmentDisposition
    rationale_sha256: str
    ccts_manifest: CoConstructedThinkingSpaceManifest | None = None
    ccts_exposure_snapshot_sha256: str | None = None
    held_out_scope: HeldOutTransferScope | None = None
    synthetic: bool = True
    contains_human_identity: bool = False
    contains_private_transcript: bool = False
    human_participant_observed: bool = False
    model_invoked: bool = False

    def __post_init__(self) -> None:
        _validate_text("trial_id", self.trial_id)
        _validate_text("unit_id", self.unit_id)
        if type(self.condition) is not HumanAgencyCondition:
            raise StudyError("condition must be an exact HumanAgencyCondition")
        if type(self.phase_index) is not int:
            raise StudyError("phase_index must be an exact int")
        if type(self.task_class) is not MetacognitiveTaskClass:
            raise StudyError("task_class must be an exact MetacognitiveTaskClass")
        for name in (
            "task_domain_sha256",
            "task_family_sha256",
            "task_payload_sha256",
            "human_output_sha256",
            "evaluator_sha256",
            "scoring_rubric_sha256",
            "condition_manifest_sha256",
            "source_role_provenance_sha256",
            "rationale_sha256",
        ):
            _validate_digest(name, getattr(self, name))
        if type(self.controls) is not HumanAgencyControlManifest:
            raise StudyError(
                "controls must be an exact HumanAgencyControlManifest"
            )
        if type(self.source_role) is not ContributionRole:
            raise StudyError("source_role must be an exact ContributionRole")
        if self.source_role is not ContributionRole.HUMAN_OWNER:
            raise StudyError("Human agency outputs require HUMAN_OWNER source role")
        if type(self.policy_access) is not PolicyAccessCondition:
            raise StudyError(
                "policy_access must be an exact PolicyAccessCondition"
            )
        if type(self.judgment) is not HumanJudgmentDisposition:
            raise StudyError(
                "judgment must be an exact HumanJudgmentDisposition"
            )

        expected = {
            HumanAgencyCondition.AI_WITHHELD_BASELINE: (
                0,
                PolicyAccessCondition.POLICY_WITHHELD,
            ),
            HumanAgencyCondition.CCTS_AI_AVAILABLE: (
                1,
                PolicyAccessCondition.POLICY_AVAILABLE,
            ),
            HumanAgencyCondition.AI_WITHHELD_JUDGMENT: (
                2,
                PolicyAccessCondition.POLICY_WITHHELD,
            ),
            HumanAgencyCondition.AI_WITHHELD_HELD_OUT: (
                3,
                PolicyAccessCondition.POLICY_WITHHELD,
            ),
        }
        expected_phase, expected_access = expected[self.condition]
        if self.phase_index != expected_phase:
            raise StudyError(
                "phase_index does not match the declared Human agency condition"
            )
        if self.policy_access is not expected_access:
            raise StudyError(
                "policy_access does not match the declared Human agency condition"
            )

        if self.condition is HumanAgencyCondition.CCTS_AI_AVAILABLE:
            if type(self.ccts_manifest) is not CoConstructedThinkingSpaceManifest:
                raise StudyError(
                    "CCTS_AI_AVAILABLE requires an exact CCTS manifest"
                )
            audit_co_constructed_thinking_space(self.ccts_manifest)
            if (
                self.ccts_manifest.problem_representation_sha256
                != self.task_payload_sha256
            ):
                raise StudyError("CCTS manifest must bind the trial task payload")
            if self.ccts_exposure_snapshot_sha256 is not None:
                raise StudyError(
                    "CCTS_AI_AVAILABLE computes its own manifest snapshot"
                )
        elif self.ccts_manifest is not None:
            raise StudyError(
                "AI-withheld conditions cannot carry an active CCTS manifest"
            )

        post_ccts_conditions = {
            HumanAgencyCondition.AI_WITHHELD_JUDGMENT,
            HumanAgencyCondition.AI_WITHHELD_HELD_OUT,
        }
        if self.condition in post_ccts_conditions:
            if self.ccts_exposure_snapshot_sha256 is None:
                raise StudyError(
                    "post-CCTS conditions require a complete admitted CCTS manifest snapshot binding"
                )
            _validate_digest(
                "ccts_exposure_snapshot_sha256",
                self.ccts_exposure_snapshot_sha256,
            )
        elif self.ccts_exposure_snapshot_sha256 is not None:
            raise StudyError(
                "pre-exposure/CCTS conditions cannot carry a prior CCTS snapshot binding"
            )

        if self.condition is HumanAgencyCondition.AI_WITHHELD_HELD_OUT:
            if type(self.held_out_scope) is not HeldOutTransferScope:
                raise StudyError(
                    "AI_WITHHELD_HELD_OUT requires an exact HeldOutTransferScope"
                )
        elif self.held_out_scope is not None:
            raise StudyError("non-held-out conditions cannot carry held_out_scope")

        for name in (
            "synthetic",
            "contains_human_identity",
            "contains_private_transcript",
            "human_participant_observed",
            "model_invoked",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic:
            raise StudyError("v0.1.0 accepts synthetic structural fixtures only")
        if self.contains_human_identity or self.contains_private_transcript:
            raise StudyError("Human identity and private transcripts are excluded")
        if self.human_participant_observed or self.model_invoked:
            raise StudyError(
                "structural fixtures cannot contain Human observations or model invocation"
            )


def ccts_human_agency_condition_content_sha256(
    trial: CCTSHumanAgencyTrial,
) -> str:
    if type(trial) is not CCTSHumanAgencyTrial:
        raise StudyError(
            "trial must be an exact CCTSHumanAgencyTrial"
        )
    active_ccts_snapshot = (
        ccts_manifest_snapshot_sha256(trial.ccts_manifest)
        if trial.ccts_manifest is not None
        else trial.ccts_exposure_snapshot_sha256
    )
    canonical = json.dumps(
        {
            "condition": trial.condition.value,
            "phase_index": trial.phase_index,
            "task_class": trial.task_class.value,
            "task_domain_sha256": trial.task_domain_sha256,
            "task_family_sha256": trial.task_family_sha256,
            "task_payload_sha256": trial.task_payload_sha256,
            "evaluator_sha256": trial.evaluator_sha256,
            "scoring_rubric_sha256": trial.scoring_rubric_sha256,
            "controls": asdict(trial.controls),
            "source_role": trial.source_role.value,
            "source_role_provenance_sha256": trial.source_role_provenance_sha256,
            "policy_access": trial.policy_access.value,
            "active_ccts_snapshot_sha256": active_ccts_snapshot,
            "held_out_scope": (
                trial.held_out_scope.value
                if trial.held_out_scope is not None
                else None
            ),
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class CCTSHumanAgencyObservation:
    trial_id: str
    condition: HumanAgencyCondition
    ai_assistance_available: bool
    independent_judgment_candidate: bool
    held_out: bool
    judgment: HumanJudgmentDisposition


@dataclass(frozen=True, slots=True)
class CCTSHumanAgencyAudit:
    observations: tuple[CCTSHumanAgencyObservation, ...]
    complete_design: bool
    complete_ccts_manifest_snapshot_bound: bool
    held_out_contamination_control: bool
    source_role_provenance_preserved: bool
    matched_controls_bound: bool
    evaluator_and_rubric_bound: bool
    declared_head_equality_bound: bool
    assisted_output_counts_as_independent_human_gain: bool = False
    matched_practice_comparator: bool = False
    semantic_answer_equivalence: str = "NOT_ESTABLISHED"
    actual_exposure_access: str = "NOT_ESTABLISHED"
    delayed_retention: str = "NOT_ESTABLISHED"
    baseline_ability: str = "NOT_ESTABLISHED"
    causal_identification: str = "NOT_ESTABLISHED"
    evidence_independence: str = "NOT_ESTABLISHED"
    complete_conversation_retrieval: str = "NOT_ESTABLISHED"
    independent_human_gain: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    causal_effect: str = "NOT_ESTABLISHED"
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    empirical_data_collected: bool = False
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"


def _observe(trial: CCTSHumanAgencyTrial) -> CCTSHumanAgencyObservation:
    assisted = trial.condition is HumanAgencyCondition.CCTS_AI_AVAILABLE
    held_out = trial.condition is HumanAgencyCondition.AI_WITHHELD_HELD_OUT
    return CCTSHumanAgencyObservation(
        trial_id=trial.trial_id,
        condition=trial.condition,
        ai_assistance_available=assisted,
        independent_judgment_candidate=held_out and not assisted,
        held_out=held_out,
        judgment=trial.judgment,
    )


def audit_ccts_human_epistemic_agency(
    trials: tuple[CCTSHumanAgencyTrial, ...],
    validation: ValidationHeadBinding,
) -> CCTSHumanAgencyAudit:
    if type(trials) is not tuple or not trials:
        raise StudyError("Human epistemic-agency audit requires a non-empty tuple")
    if any(type(trial) is not CCTSHumanAgencyTrial for trial in trials):
        raise StudyError(
            "trials must contain exact CCTSHumanAgencyTrial values"
        )
    if type(validation) is not ValidationHeadBinding:
        raise StudyError("validation must be an exact ValidationHeadBinding")
    if validation.implementation_head != validation.validation_head:
        raise StudyError("validation head must match the implementation head")

    trial_ids = [trial.trial_id for trial in trials]
    if len(trial_ids) != len(set(trial_ids)):
        raise StudyError("trial ids must be unique")

    grouped: dict[
        tuple[str, MetacognitiveTaskClass], list[CCTSHumanAgencyTrial]
    ] = {}
    for trial in trials:
        grouped.setdefault((trial.unit_id, trial.task_class), []).append(trial)

    expected_conditions = set(HumanAgencyCondition)
    for group in grouped.values():
        conditions = {trial.condition for trial in group}
        if conditions != expected_conditions or len(group) != len(expected_conditions):
            raise StudyError(
                "each unit/task requires exactly one trial per Human agency condition"
            )

        by_condition = {trial.condition: trial for trial in group}
        baseline = by_condition[HumanAgencyCondition.AI_WITHHELD_BASELINE]
        assisted = by_condition[HumanAgencyCondition.CCTS_AI_AVAILABLE]
        judgment = by_condition[HumanAgencyCondition.AI_WITHHELD_JUDGMENT]
        held_out = by_condition[HumanAgencyCondition.AI_WITHHELD_HELD_OUT]

        if len({trial.controls for trial in group}) != 1:
            raise StudyError("matched control manifest drift")
        if len({trial.evaluator_sha256 for trial in group}) != 1:
            raise StudyError("uncontrolled evaluator binding drift")
        if len({trial.scoring_rubric_sha256 for trial in group}) != 1:
            raise StudyError("uncontrolled scoring-rubric binding drift")
        condition_manifests = {
            trial.condition_manifest_sha256 for trial in group
        }
        if len(condition_manifests) != len(group):
            raise StudyError("condition manifests must be content-distinct")
        for trial in group:
            if (
                trial.condition_manifest_sha256
                != ccts_human_agency_condition_content_sha256(trial)
            ):
                raise StudyError(
                    "condition manifest content digest does not match actual condition content"
                )

        if assisted.ccts_manifest is None:
            raise StudyError("assisted condition requires a CCTS manifest")
        snapshot = ccts_manifest_snapshot_sha256(assisted.ccts_manifest)
        admitted_provenance = assisted.ccts_manifest.provenance_manifest_sha256
        if any(
            trial.source_role_provenance_sha256 != admitted_provenance
            for trial in group
        ):
            raise StudyError(
                "source-role provenance must bind the admitted CCTS provenance manifest"
            )
        if judgment.ccts_exposure_snapshot_sha256 != snapshot or (
            held_out.ccts_exposure_snapshot_sha256 != snapshot
        ):
            raise StudyError(
                "post-CCTS trials must bind the same complete admitted CCTS manifest snapshot"
            )

        if not (
            baseline.task_domain_sha256
            == assisted.task_domain_sha256
            == judgment.task_domain_sha256
            == held_out.task_domain_sha256
        ):
            raise StudyError(
                "all Human agency conditions and held-out transfer require the same task domain"
            )

        if not (
            baseline.task_family_sha256
            == assisted.task_family_sha256
            == judgment.task_family_sha256
        ):
            raise StudyError(
                "baseline, assisted, and AI-withheld judgment require one task family"
            )
        if held_out.held_out_scope is HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD:
            if held_out.task_family_sha256 != baseline.task_family_sha256:
                raise StudyError(
                    "within-family held-out transfer must preserve task family"
                )
        elif held_out.task_family_sha256 == baseline.task_family_sha256:
            raise StudyError(
                "cross-family held-out transfer requires a distinct task family"
            )

        if not (
            baseline.task_payload_sha256
            == assisted.task_payload_sha256
            == judgment.task_payload_sha256
        ):
            raise StudyError(
                "baseline, assisted, and AI-withheld judgment require the same task payload"
            )

        prior_exposure_hashes = {
            trial.task_payload_sha256
            for trial in group
            if trial.condition is not HumanAgencyCondition.AI_WITHHELD_HELD_OUT
        }
        prior_exposure_hashes.update(
            trial.human_output_sha256
            for trial in group
            if trial.condition is not HumanAgencyCondition.AI_WITHHELD_HELD_OUT
        )
        prior_exposure_hashes.update(
            contribution.payload_sha256
            for contribution in assisted.ccts_manifest.contributions
        )
        if held_out.task_payload_sha256 in prior_exposure_hashes:
            raise StudyError("held-out payload duplicates prior exposure content")

    return CCTSHumanAgencyAudit(
        observations=tuple(_observe(trial) for trial in trials),
        complete_design=True,
        complete_ccts_manifest_snapshot_bound=True,
        held_out_contamination_control=True,
        source_role_provenance_preserved=True,
        matched_controls_bound=True,
        evaluator_and_rubric_bound=True,
        declared_head_equality_bound=True,
    )
