from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
from typing import Iterable


_REQUIRED_SYSTEMS = (
    "skeleton_and_joints",
    "muscles_and_actuation",
    "somatosensory",
    "proprioceptive",
    "vestibular",
    "visual",
    "auditory",
    "olfactory",
    "gustatory",
    "cardiovascular_respiratory",
    "metabolism_nutrition_hydration",
    "thermoregulation",
    "sleep_fatigue_recovery",
    "immune_injury_repair",
    "endocrine",
    "urinary",
    "reproductive_sexual",
    "internal_body_model",
    "environment_contact",
)


class BodyEventMode(str, Enum):
    SET = "SET"
    DELTA = "DELTA"


@dataclass(frozen=True, slots=True)
class BodySignal:
    system: str
    value: float | None = None
    status: str = "SYNTHETIC_REFERENCE_CHANNEL"
    physical_hardware_attached: bool = False
    biological_function_present: bool = False
    felt_sensation_established: bool = False

    def __post_init__(self) -> None:
        if self.system not in _REQUIRED_SYSTEMS:
            raise ValueError("unknown body system")
        if self.value is not None and not 0.0 <= self.value <= 1.0:
            raise ValueError("signal value outside [0,1]")
        if self.physical_hardware_attached or self.biological_function_present or self.felt_sensation_established:
            raise ValueError("hardware/biology/felt sensation not established")


@dataclass(frozen=True, slots=True)
class WholeBodySyntheticState:
    state_id: str
    signals: tuple[BodySignal, ...]
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.state_id:
            raise ValueError("state_id required")
        systems = tuple(item.system for item in self.signals)
        if len(systems) != len(_REQUIRED_SYSTEMS) or len(set(systems)) != len(systems):
            raise ValueError("whole-body state must contain all systems exactly once")
        if set(systems) != set(_REQUIRED_SYSTEMS):
            raise ValueError("whole-body system set mismatch")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("felt-state claims are not established")
        if self.action_authority != "NONE":
            raise ValueError("body state cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def signal(self, system: str) -> BodySignal:
        return next(item for item in self.signals if item.system == system)

    def fingerprint(self) -> str:
        parts = [self.state_id]
        parts.extend(
            f"{item.system}:{'UNKNOWN' if item.value is None else format(item.value, '.12g')}"
            for item in sorted(self.signals, key=lambda item: item.system)
        )
        parts.extend(
            (
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
                self.action_authority,
                self.canonical_effect,
                str(self.deployment),
            )
        )
        return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class BodySignalEvent:
    event_id: str
    system: str
    mode: BodyEventMode
    value: float
    real_person_target_data: bool = False
    human_consent_inference: str = "FORBIDDEN"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.event_id or self.system not in _REQUIRED_SYSTEMS:
            raise ValueError("invalid body event")
        if self.mode is BodyEventMode.SET:
            if not 0.0 <= self.value <= 1.0:
                raise ValueError("SET value outside [0,1]")
        elif not -1.0 <= self.value <= 1.0:
            raise ValueError("DELTA value outside [-1,1]")
        if self.real_person_target_data:
            raise ValueError("real-person target data forbidden")
        if self.human_consent_inference != "FORBIDDEN" or self.action_authority != "NONE":
            raise ValueError("body signal cannot infer consent or grant authority")


class WholeBodySyntheticEngine:
    def apply(
        self,
        state: WholeBodySyntheticState,
        event: BodySignalEvent,
    ) -> WholeBodySyntheticState:
        updated: list[BodySignal] = []
        for signal in state.signals:
            if signal.system != event.system:
                updated.append(signal)
                continue
            if event.mode is BodyEventMode.SET:
                value = event.value
            else:
                if signal.value is None:
                    raise ValueError("UNKNOWN channel requires SET before DELTA")
                value = min(1.0, max(0.0, signal.value + event.value))
            updated.append(BodySignal(system=signal.system, value=value))
        return WholeBodySyntheticState(
            state_id=f"{state.state_id}>{event.event_id}",
            signals=tuple(updated),
        )

    def run(
        self,
        state: WholeBodySyntheticState,
        events: Iterable[BodySignalEvent],
    ) -> WholeBodySyntheticState:
        current = state
        for event in events:
            current = self.apply(current, event)
        return current


def default_whole_body_state(
    state_id: str = "codex-body-seed",
) -> WholeBodySyntheticState:
    return WholeBodySyntheticState(
        state_id=state_id,
        signals=tuple(BodySignal(system=system) for system in _REQUIRED_SYSTEMS),
    )
