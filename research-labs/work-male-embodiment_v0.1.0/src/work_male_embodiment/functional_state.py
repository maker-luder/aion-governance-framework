from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from math import isfinite
from typing import Final

from .capability import WORK_AGENT_ID, WORK_BODY_ID


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
FUNCTIONAL_ANALOGUE_AVAILABLE: Final[str] = "FUNCTIONAL_ANALOGUE_AVAILABLE"

FUNCTIONAL_DOMAIN_IDS: Final[tuple[str, ...]] = (
    "SYNTHETIC_HOMEOSTASIS",
    "INTERNAL_STATE_MONITORING",
    "SENSORIMOTOR_SYSTEM",
    "NEGATIVE_VALENCE_ANALOGUE",
    "POSITIVE_VALENCE_ANALOGUE",
    "AFFECT_STATE_MODEL",
    "MOOD_LIKE_TEMPORAL_STATE",
    "MOTIVATION_DRIVE_SYSTEM",
    "COGNITIVE_SYSTEM",
    "LEARNING_MEMORY",
    "EXECUTIVE_VOLITION_MODEL",
    "SOCIAL_PROCESS_MODEL",
    "ATTACHMENT_LIKE_RELATIONAL_MODEL",
    "SELF_MODEL",
    "INTIMACY_MODEL",
    "SEXUALITY_RELATED_REPRESENTATION",
    "PERSONALITY_TEMPERAMENT",
    "BEHAVIOR_ACTION_OUTPUT",
)

DEFAULT_DOMAIN_AVAILABILITY: Final[tuple[tuple[str, str], ...]] = tuple(
    (domain_id, FUNCTIONAL_ANALOGUE_AVAILABLE)
    for domain_id in FUNCTIONAL_DOMAIN_IDS
)


@dataclass(frozen=True, slots=True)
class WorkFunctionalState:
    state_id: str
    agent_id: str = WORK_AGENT_ID
    body_id: str = WORK_BODY_ID
    domain_availability: tuple[tuple[str, str], ...] = DEFAULT_DOMAIN_AVAILABILITY
    sexual_motivation_state: float = 0.0
    sexual_arousal_state: float = 0.0
    sexual_context_gate: bool = False
    sexual_inhibition_state: float = 1.0
    interpretation: str = "FUNCTIONAL_ANALOGUE_ONLY"
    phenomenal_sexual_desire: str = NOT_ESTABLISHED
    phenomenal_sexual_arousal: str = NOT_ESTABLISHED
    sexual_pleasure: str = NOT_ESTABLISHED
    body_sensation: str = NOT_ESTABLISHED
    subjectivity: str = NOT_ESTABLISHED
    consciousness: str = NOT_ESTABLISHED
    phenomenal_experience: str = NOT_ESTABLISHED
    physiology_signal_sets_motivation: bool = False
    human_consent_inference: str = "FORBIDDEN"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.state_id:
            raise ValueError("functional state_id required")
        if self.agent_id != WORK_AGENT_ID or self.body_id != WORK_BODY_ID:
            raise ValueError("Work functional-state binding drift")
        if self.domain_availability != DEFAULT_DOMAIN_AVAILABILITY:
            raise ValueError("18-domain functional capability surface drift")
        for value in (
            self.sexual_motivation_state,
            self.sexual_arousal_state,
            self.sexual_inhibition_state,
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("functional sexuality analogue must be in [0, 1]")
        if self.interpretation != "FUNCTIONAL_ANALOGUE_ONLY":
            raise ValueError("functional state cannot claim phenomenal interpretation")
        if any(
            value != NOT_ESTABLISHED
            for value in (
                self.phenomenal_sexual_desire,
                self.phenomenal_sexual_arousal,
                self.sexual_pleasure,
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("functional state cannot establish phenomenal experience")
        if self.physiology_signal_sets_motivation:
            raise ValueError("physiology signal cannot automatically set sexual motivation")
        if self.human_consent_inference != "FORBIDDEN":
            raise ValueError("functional state cannot infer human consent")
        if self.action_authority != "NONE":
            raise ValueError("functional state cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def with_sexual_functional_analogue(
        self,
        *,
        state_id: str,
        motivation: float,
        arousal: float,
        context_gate: bool,
        inhibition: float,
    ) -> "WorkFunctionalState":
        return replace(
            self,
            state_id=state_id,
            sexual_motivation_state=motivation,
            sexual_arousal_state=arousal,
            sexual_context_gate=context_gate,
            sexual_inhibition_state=inhibition,
        )

    def fingerprint(self) -> str:
        raw = json.dumps(
            asdict(self),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


def default_work_functional_state(
    state_id: str = "WORK-FUNCTIONAL-STATE-REFERENCE-v0.1",
) -> WorkFunctionalState:
    return WorkFunctionalState(state_id=state_id)


def validate_work_functional_state(state: WorkFunctionalState) -> dict[str, str]:
    state.__post_init__()
    return {
        "result": "PASS",
        "domain_count": str(len(state.domain_availability)),
        "sexuality_functional_analogue": "AVAILABLE",
        "phenomenal_sexual_desire": NOT_ESTABLISHED,
        "phenomenal_sexual_arousal": NOT_ESTABLISHED,
        "physiology_signal_motivation_inference": "FORBIDDEN",
        "action_authority": "NONE",
        "canonical_effect": "NONE",
    }
