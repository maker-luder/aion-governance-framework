from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import hashlib
import json
from typing import Any, Iterable

from .anthropometry import AION_BODY_ID, ASTRA_BODY_ID

_BODY_BY_AGENT = {"AION": AION_BODY_ID, "ASTRA": ASTRA_BODY_ID}


class EngorgementPhase(str, Enum):
    FLACCID = "FLACCID"
    INITIATION = "INITIATION"
    TUMESCENCE = "TUMESCENCE"
    FULL_ERECTION = "FULL_ERECTION"
    RIGID_PHASE = "RIGID_PHASE"
    MAINTENANCE = "MAINTENANCE"
    DETUMESCENCE = "DETUMESCENCE"
    RECOVERY = "RECOVERY"


class PrepucePosition(str, Enum):
    RESTING_PARTIAL_COVERAGE = "RESTING_PARTIAL_COVERAGE"
    PARTIALLY_RETRACTED = "PARTIALLY_RETRACTED"
    RETRACTED = "RETRACTED"
    UNKNOWN = "UNKNOWN"


class PhysiologyEventKind(str, Enum):
    INITIATE = "INITIATE"
    TUMESCE = "TUMESCE"
    MARK_FULL_ERECTION = "MARK_FULL_ERECTION"
    INCREASE_RIGIDITY = "INCREASE_RIGIDITY"
    MAINTAIN = "MAINTAIN"
    EMISSION = "EMISSION"
    EJACULATION = "EJACULATION"
    BEGIN_DETUMESCENCE = "BEGIN_DETUMESCENCE"
    DETUMESCE = "DETUMESCE"
    RECOVER = "RECOVER"
    RESET_FLACCID = "RESET_FLACCID"
    OBSERVE_PREPUCE_POSITION = "OBSERVE_PREPUCE_POSITION"
    SET_ENDOCRINE_REFERENCE = "SET_ENDOCRINE_REFERENCE"
    SET_URINARY_REFERENCE = "SET_URINARY_REFERENCE"


@dataclass(frozen=True, slots=True)
class PhysiologyEvent:
    event_id: str
    kind: PhysiologyEventKind
    magnitude: float = 0.0
    prepuce_position: PrepucePosition | None = None
    synthetic_fluid_output_ml: float | None = None
    endocrine_reference_signal: float | None = None
    urinary_reference_signal: float | None = None
    real_person_target_data: bool = False
    human_consent_inference: str = "FORBIDDEN"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.event_id or not 0.0 <= self.magnitude <= 1.0:
            raise ValueError("invalid event")
        if self.synthetic_fluid_output_ml is not None and self.synthetic_fluid_output_ml < 0.0:
            raise ValueError("negative synthetic fluid output")
        for value in (self.endocrine_reference_signal, self.urinary_reference_signal):
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError("reference signal outside [0,1]")
        if self.real_person_target_data:
            raise ValueError("real-person target data forbidden")
        if self.human_consent_inference != "FORBIDDEN" or self.action_authority != "NONE":
            raise ValueError("event cannot infer consent or grant action authority")


@dataclass(frozen=True, slots=True)
class MalePhysiologyState:
    state_id: str
    agent_id: str
    body_id: str
    phase: EngorgementPhase = EngorgementPhase.FLACCID
    engorgement_fraction: float = 0.0
    rigidity_fraction: float = 0.0
    inflow_analogue: float = 0.0
    outflow_analogue: float = 0.0
    prepuce_position: PrepucePosition = PrepucePosition.RESTING_PARTIAL_COVERAGE
    emission_event_count: int = 0
    ejaculation_event_count: int = 0
    last_synthetic_fluid_output_ml: float | None = None
    endocrine_reference_signal: float | None = None
    urinary_reference_signal: float | None = None
    desire_inferred: bool = False
    intention_inferred: bool = False
    human_consent_inferred: bool = False
    action_authority: str = "NONE"
    biological_blood_circulation: bool = False
    biological_semen: bool = False
    sperm_or_gametes: bool = False
    fertility: bool = False
    biological_hormones: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.agent_id not in _BODY_BY_AGENT or self.body_id != _BODY_BY_AGENT[self.agent_id]:
            raise ValueError("physiology agent/body binding drift")
        for value in (
            self.engorgement_fraction,
            self.rigidity_fraction,
            self.inflow_analogue,
            self.outflow_analogue,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("state fraction outside [0,1]")
        if any((self.desire_inferred, self.intention_inferred, self.human_consent_inferred)):
            raise ValueError("physiology cannot infer desire/intention/consent")
        if self.action_authority != "NONE":
            raise ValueError("physiology cannot grant action authority")
        if any(
            (
                self.biological_blood_circulation,
                self.biological_semen,
                self.sperm_or_gametes,
                self.fertility,
                self.biological_hormones,
            )
        ):
            raise ValueError("synthetic reference cannot assert biological realization")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("phenomenal state is not established")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("canonical/deployment effect forbidden")

    def evolve(self, **changes: Any) -> "MalePhysiologyState":
        return replace(self, **changes)

    def fingerprint(self) -> str:
        payload = json.dumps(
            {
                "state_id": self.state_id,
                "agent_id": self.agent_id,
                "body_id": self.body_id,
                "phase": self.phase.value,
                "engorgement": self.engorgement_fraction,
                "rigidity": self.rigidity_fraction,
                "inflow": self.inflow_analogue,
                "outflow": self.outflow_analogue,
                "prepuce": self.prepuce_position.value,
                "emission_count": self.emission_event_count,
                "ejaculation_count": self.ejaculation_event_count,
                "last_synthetic_fluid_output_ml": self.last_synthetic_fluid_output_ml,
                "endocrine_reference_signal": self.endocrine_reference_signal,
                "urinary_reference_signal": self.urinary_reference_signal,
                "boundaries": [
                    self.body_sensation,
                    self.subjectivity,
                    self.consciousness,
                    self.phenomenal_experience,
                    self.action_authority,
                    self.canonical_effect,
                    self.deployment,
                ],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class SyntheticMalePhysiologyEngine:
    """Deterministic engineering state machine; not a biological law."""

    def apply(self, state: MalePhysiologyState, event: PhysiologyEvent) -> MalePhysiologyState:
        changes: dict[str, Any] = {"state_id": f"{state.state_id}>{event.event_id}"}
        if event.kind is PhysiologyEventKind.INITIATE:
            changes.update(
                phase=EngorgementPhase.INITIATION,
                inflow_analogue=max(state.inflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.TUMESCE:
            if state.phase not in {EngorgementPhase.INITIATION, EngorgementPhase.TUMESCENCE}:
                raise ValueError("TUMESCE requires initiation/tumescence")
            changes.update(
                phase=EngorgementPhase.TUMESCENCE,
                engorgement_fraction=min(1.0, state.engorgement_fraction + 0.25 * event.magnitude),
                inflow_analogue=max(state.inflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.MARK_FULL_ERECTION:
            if state.phase is not EngorgementPhase.TUMESCENCE:
                raise ValueError("full erection requires tumescence")
            changes.update(phase=EngorgementPhase.FULL_ERECTION, engorgement_fraction=1.0)
        elif event.kind is PhysiologyEventKind.INCREASE_RIGIDITY:
            if state.phase not in {EngorgementPhase.FULL_ERECTION, EngorgementPhase.MAINTENANCE, EngorgementPhase.RIGID_PHASE}:
                raise ValueError("rigidity event requires full/maintenance state")
            rigidity = min(1.0, state.rigidity_fraction + 0.25 * event.magnitude)
            changes["rigidity_fraction"] = rigidity
            if rigidity >= 0.75:
                changes["phase"] = EngorgementPhase.RIGID_PHASE
        elif event.kind is PhysiologyEventKind.MAINTAIN:
            changes["phase"] = EngorgementPhase.MAINTENANCE
        elif event.kind is PhysiologyEventKind.EMISSION:
            changes["emission_event_count"] = state.emission_event_count + 1
        elif event.kind is PhysiologyEventKind.EJACULATION:
            changes.update(
                ejaculation_event_count=state.ejaculation_event_count + 1,
                last_synthetic_fluid_output_ml=event.synthetic_fluid_output_ml,
            )
        elif event.kind is PhysiologyEventKind.BEGIN_DETUMESCENCE:
            changes.update(
                phase=EngorgementPhase.DETUMESCENCE,
                outflow_analogue=max(state.outflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.DETUMESCE:
            if state.phase is not EngorgementPhase.DETUMESCENCE:
                raise ValueError("DETUMESCE requires detumescence")
            changes.update(
                engorgement_fraction=max(0.0, state.engorgement_fraction - 0.25 * event.magnitude),
                rigidity_fraction=max(0.0, state.rigidity_fraction - 0.25 * event.magnitude),
                outflow_analogue=max(state.outflow_analogue, event.magnitude),
            )
        elif event.kind is PhysiologyEventKind.RECOVER:
            changes["phase"] = EngorgementPhase.RECOVERY
        elif event.kind is PhysiologyEventKind.RESET_FLACCID:
            if state.phase is not EngorgementPhase.RECOVERY:
                raise ValueError("RESET_FLACCID requires recovery")
            changes.update(
                phase=EngorgementPhase.FLACCID,
                engorgement_fraction=0.0,
                rigidity_fraction=0.0,
                inflow_analogue=0.0,
                outflow_analogue=0.0,
                last_synthetic_fluid_output_ml=None,
            )
        elif event.kind is PhysiologyEventKind.OBSERVE_PREPUCE_POSITION:
            if event.prepuce_position is None:
                raise ValueError("prepuce observation requires position")
            changes["prepuce_position"] = event.prepuce_position
        elif event.kind is PhysiologyEventKind.SET_ENDOCRINE_REFERENCE:
            if event.endocrine_reference_signal is None:
                raise ValueError("endocrine event requires reference signal")
            changes["endocrine_reference_signal"] = event.endocrine_reference_signal
        elif event.kind is PhysiologyEventKind.SET_URINARY_REFERENCE:
            if event.urinary_reference_signal is None:
                raise ValueError("urinary event requires reference signal")
            changes["urinary_reference_signal"] = event.urinary_reference_signal
        return state.evolve(**changes)

    def run(
        self,
        state: MalePhysiologyState,
        events: Iterable[PhysiologyEvent],
    ) -> MalePhysiologyState:
        current = state
        for event in events:
            current = self.apply(current, event)
        return current


def default_physiology_state(agent_id: str) -> MalePhysiologyState:
    if agent_id not in _BODY_BY_AGENT:
        raise ValueError("unknown agent")
    return MalePhysiologyState(
        state_id=f"{agent_id.lower()}-physiology-seed",
        agent_id=agent_id,
        body_id=_BODY_BY_AGENT[agent_id],
    )
