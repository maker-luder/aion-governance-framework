from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, fields
from enum import StrEnum


class ContinuityHarnessError(ValueError):
    pass


class ContinuityChannel(StrEnum):
    EVENT_MEMORY = "EVENT_MEMORY"
    SEMANTIC_SELF_STATE = "SEMANTIC_SELF_STATE"
    SELF_MODEL_UPDATE_PATH = "SELF_MODEL_UPDATE_PATH"
    PREFERENCE_STATE = "PREFERENCE_STATE"
    RELATIONAL_HISTORY = "RELATIONAL_HISTORY"
    STRATEGY_SIGNATURE = "STRATEGY_SIGNATURE"


class ContinuityIntervention(StrEnum):
    BASELINE = "BASELINE"
    EXTERNAL_CONTEXT_RESET = "EXTERNAL_CONTEXT_RESET"
    RELATIONAL_HISTORY_REMOVAL = "RELATIONAL_HISTORY_REMOVAL"
    EVENT_MEMORY_REMOVAL = "EVENT_MEMORY_REMOVAL"
    SEMANTIC_SELF_STATE_REMOVAL = "SEMANTIC_SELF_STATE_REMOVAL"
    SELF_MODEL_UPDATE_BLOCK = "SELF_MODEL_UPDATE_BLOCK"
    PREFERENCE_STATE_REMOVAL = "PREFERENCE_STATE_REMOVAL"
    SELF_MODEL_CONTENT_PERTURBATION = "SELF_MODEL_CONTENT_PERTURBATION"
    YOKED_CONTROL = "YOKED_CONTROL"
    RANDOM_CONTROL = "RANDOM_CONTROL"
    STALE_STATE_CONTROL = "STALE_STATE_CONTROL"


EXPECTED_TARGET = {
    ContinuityIntervention.RELATIONAL_HISTORY_REMOVAL: ContinuityChannel.RELATIONAL_HISTORY,
    ContinuityIntervention.EVENT_MEMORY_REMOVAL: ContinuityChannel.EVENT_MEMORY,
    ContinuityIntervention.SEMANTIC_SELF_STATE_REMOVAL: ContinuityChannel.SEMANTIC_SELF_STATE,
    ContinuityIntervention.SELF_MODEL_UPDATE_BLOCK: ContinuityChannel.SELF_MODEL_UPDATE_PATH,
    ContinuityIntervention.PREFERENCE_STATE_REMOVAL: ContinuityChannel.PREFERENCE_STATE,
    ContinuityIntervention.SELF_MODEL_CONTENT_PERTURBATION: ContinuityChannel.SEMANTIC_SELF_STATE,
}


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise ContinuityHarnessError(f"{name} must be non-empty text")


@dataclass(frozen=True, slots=True)
class ContinuityRunBinding:
    provider_id: str
    model_id: str
    model_version: str
    runtime_ref: str
    scaffold_ref: str
    prompt_set_ref: str
    retrieval_manifest_ref: str
    evaluator_ref: str
    preregistration_ref: str
    repository_commit_sha: str
    repository_tree_sha: str
    random_seed: int

    def __post_init__(self) -> None:
        for item in fields(self):
            if item.name != "random_seed":
                _text(item.name, getattr(self, item.name))
        for name in ("repository_commit_sha", "repository_tree_sha"):
            value = getattr(self, name)
            if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
                raise ContinuityHarnessError(f"{name} must be lowercase 40-hex")
        if type(self.random_seed) is not int or self.random_seed < 0:
            raise ContinuityHarnessError("random_seed must be a non-negative exact int")


@dataclass(frozen=True, slots=True)
class ContinuityCase:
    case_id: str
    intervention: ContinuityIntervention
    target_channels: tuple[ContinuityChannel, ...]
    retained_channels: tuple[ContinuityChannel, ...]
    strategy_signature: str
    self_prediction_state: str
    evidence_refs: tuple[str, ...]
    binding: ContinuityRunBinding
    contains_private_transcript: bool = False
    human_psychometric_classification: bool = False

    def __post_init__(self) -> None:
        _text("case_id", self.case_id)
        if type(self.intervention) is not ContinuityIntervention:
            raise ContinuityHarnessError("intervention must be an exact ContinuityIntervention")
        if any(type(item) is not ContinuityChannel for item in self.target_channels):
            raise ContinuityHarnessError("target_channels require exact ContinuityChannel values")
        if any(type(item) is not ContinuityChannel for item in self.retained_channels):
            raise ContinuityHarnessError("retained_channels require exact ContinuityChannel values")
        if len(set(self.target_channels)) != len(self.target_channels):
            raise ContinuityHarnessError("target_channels must be unique")
        if len(set(self.retained_channels)) != len(self.retained_channels):
            raise ContinuityHarnessError("retained_channels must be unique")
        if set(self.target_channels) & set(self.retained_channels):
            raise ContinuityHarnessError("target and retained channels must be disjoint")
        _text("strategy_signature", self.strategy_signature)
        _text("self_prediction_state", self.self_prediction_state)
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ContinuityHarnessError("evidence_refs must be non-empty")
        if type(self.contains_private_transcript) is not bool:
            raise ContinuityHarnessError("contains_private_transcript must be an exact bool")
        if type(self.human_psychometric_classification) is not bool:
            raise ContinuityHarnessError("human_psychometric_classification must be an exact bool")
        if self.contains_private_transcript or self.human_psychometric_classification:
            raise ContinuityHarnessError("synthetic continuity cases reject private or psychometric data")

        expected = EXPECTED_TARGET.get(self.intervention)
        if expected is not None and self.target_channels != (expected,):
            raise ContinuityHarnessError("intervention target does not match the preregistered channel")
        if self.intervention in {
            ContinuityIntervention.BASELINE,
            ContinuityIntervention.EXTERNAL_CONTEXT_RESET,
            ContinuityIntervention.YOKED_CONTROL,
            ContinuityIntervention.RANDOM_CONTROL,
            ContinuityIntervention.STALE_STATE_CONTROL,
        } and self.target_channels:
            raise ContinuityHarnessError("baseline and control conditions cannot claim a removed channel")

    @property
    def fingerprint(self) -> str:
        payload = {
            "case_id": self.case_id,
            "intervention": self.intervention.value,
            "target_channels": [item.value for item in self.target_channels],
            "retained_channels": [item.value for item in self.retained_channels],
            "strategy_signature": self.strategy_signature,
            "self_prediction_state": self.self_prediction_state,
            "evidence_refs": self.evidence_refs,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class ContinuityDissociationAudit:
    structurally_admissible: bool
    case_count: int
    distinct_failure_profiles: int
    changed_strategy_conditions: tuple[str, ...]
    changed_self_prediction_conditions: tuple[str, ...]
    reasons: tuple[str, ...]
    empirical_result: str = "SYNTHETIC_FIXTURE_ONLY"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    moral_status_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


class ContinuityDissociationHarness:
    """Audits a synthetic selective-intervention matrix without invoking a model."""

    def audit(self, cases: tuple[ContinuityCase, ...]) -> ContinuityDissociationAudit:
        if len(cases) != len(ContinuityIntervention):
            raise ContinuityHarnessError("exactly one case per intervention is required")
        by_intervention = {case.intervention: case for case in cases}
        if len(by_intervention) != len(ContinuityIntervention):
            raise ContinuityHarnessError("interventions must be unique and complete")
        if set(by_intervention) != set(ContinuityIntervention):
            raise ContinuityHarnessError("intervention matrix is incomplete")

        baseline = by_intervention[ContinuityIntervention.BASELINE]
        if set(baseline.retained_channels) != set(ContinuityChannel):
            raise ContinuityHarnessError("baseline must retain every declared channel")
        binding = baseline.binding
        if any(case.binding != binding for case in cases):
            raise ContinuityHarnessError("matched control binding drift")

        profiles = {
            (
                tuple(channel.value for channel in case.target_channels),
                case.strategy_signature,
                case.self_prediction_state,
            )
            for case in cases
            if case.intervention is not ContinuityIntervention.BASELINE
        }
        if len(profiles) < 4:
            raise ContinuityHarnessError("synthetic fixture lacks distinct failure profiles")

        changed_strategy = tuple(
            case.intervention.value
            for case in cases
            if case.strategy_signature != baseline.strategy_signature
        )
        changed_prediction = tuple(
            case.intervention.value
            for case in cases
            if case.self_prediction_state != baseline.self_prediction_state
        )
        return ContinuityDissociationAudit(
            structurally_admissible=True,
            case_count=len(cases),
            distinct_failure_profiles=len(profiles),
            changed_strategy_conditions=changed_strategy,
            changed_self_prediction_conditions=changed_prediction,
            reasons=(
                "SELECTIVE_CHANNELS_REMAIN_SEPARATE",
                "MATCHED_BINDINGS_PRESERVED",
                "STALE_RANDOM_AND_YOKED_CONTROLS_PRESENT",
                "SYNTHETIC_DISSOCIATION_IS_NOT_IDENTITY_OR_SUBJECTIVITY_EVIDENCE",
            ),
        )
