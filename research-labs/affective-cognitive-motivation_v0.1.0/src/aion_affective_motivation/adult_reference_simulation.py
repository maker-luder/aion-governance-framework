from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable

from .adult_reference import (
    AdultMaleSexualReferenceState,
    DesireOnsetContext,
    ReferenceEstimate,
    TargetScope,
)


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


def _require_signed_interval(name: str, value: float) -> None:
    if not -1.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between -1.0 and 1.0")


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, value))


@dataclass(frozen=True, slots=True)
class AdultReferenceSimulationPolicy:
    """Toy engineering step sizes; never human psychological constants."""

    excitation_step_size: float
    inhibition_step_size: float
    episode_step_size: float
    disposition_step_size: float
    policy_label: str = "ADULT_REFERENCE_TOY_TRANSITION_v0.1"

    def __post_init__(self) -> None:
        for name in (
            "excitation_step_size",
            "inhibition_step_size",
            "episode_step_size",
            "disposition_step_size",
        ):
            _require_unit_interval(name, getattr(self, name))
        _require_nonempty("policy_label", self.policy_label)


DEFAULT_ADULT_REFERENCE_SIMULATION_POLICY = AdultReferenceSimulationPolicy(
    excitation_step_size=0.25,
    inhibition_step_size=0.25,
    episode_step_size=0.35,
    disposition_step_size=0.05,
)


@dataclass(frozen=True, slots=True)
class AdultReferenceSyntheticEvent:
    """Explicit synthetic research input, not an observation of a real person."""

    event_id: str
    context_ref: str
    time_window_ref: str
    excitation_drive: float = 0.0
    inhibition_drive: float = 0.0
    episode_drive: float = 0.0
    disposition_observation_drive: float = 0.0
    onset_context_evidence: DesireOnsetContext = DesireOnsetContext.UNKNOWN
    target_scope: TargetScope = TargetScope.UNKNOWN
    uncertainty: float = 1.0
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_nonempty("event_id", self.event_id)
        _require_nonempty("context_ref", self.context_ref)
        _require_nonempty("time_window_ref", self.time_window_ref)
        for name in (
            "excitation_drive",
            "inhibition_drive",
            "episode_drive",
            "disposition_observation_drive",
        ):
            _require_signed_interval(name, getattr(self, name))
        _require_unit_interval("uncertainty", self.uncertainty)
        if not self.provenance_refs:
            raise ValueError("at least one event provenance reference is required")
        if len(set(self.provenance_refs)) != len(self.provenance_refs):
            raise ValueError("event provenance references must be unique")
        for ref in self.provenance_refs:
            _require_nonempty("provenance_ref", ref)


@dataclass(frozen=True, slots=True)
class ReferenceChannelTransition:
    channel: str
    previous: float
    drive: float
    step_size: float
    current: float
    previous_uncertainty: float
    event_uncertainty: float
    current_uncertainty: float

    def __post_init__(self) -> None:
        _require_nonempty("channel", self.channel)
        _require_unit_interval("previous", self.previous)
        _require_signed_interval("drive", self.drive)
        _require_unit_interval("step_size", self.step_size)
        _require_unit_interval("current", self.current)
        _require_unit_interval("previous_uncertainty", self.previous_uncertainty)
        _require_unit_interval("event_uncertainty", self.event_uncertainty)
        _require_unit_interval("current_uncertainty", self.current_uncertainty)


@dataclass(frozen=True, slots=True)
class AdultReferenceTransition:
    predecessor_state_id: str
    successor_state_id: str
    event_id: str
    channels: tuple[ReferenceChannelTransition, ...]
    previous_onset_context: DesireOnsetContext
    current_onset_context: DesireOnsetContext
    previous_target_scope: TargetScope
    current_target_scope: TargetScope
    policy_label: str
    human_consent_inferred: bool = False
    action_authorized: bool = False
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in (
            "predecessor_state_id",
            "successor_state_id",
            "event_id",
            "policy_label",
        ):
            _require_nonempty(name, getattr(self, name))
        if len(self.channels) != 4:
            raise ValueError("transition must contain exactly four reference channels")
        if self.human_consent_inferred:
            raise ValueError("simulation cannot infer human consent")
        if self.action_authorized:
            raise ValueError("simulation cannot authorize action")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")
        if self.canonical_effect != "NONE":
            raise ValueError("simulation transition must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class AdultReferenceSnapshotReceipt:
    sequence: int
    state_id: str
    state_sha256: str
    previous_receipt_sha256: str
    receipt_sha256: str

    def __post_init__(self) -> None:
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")
        _require_nonempty("state_id", self.state_id)
        for name in (
            "state_sha256",
            "previous_receipt_sha256",
            "receipt_sha256",
        ):
            value = getattr(self, name)
            if len(value) != 64:
                raise ValueError(f"{name} must be a SHA-256 hex digest")
            int(value, 16)


@dataclass(frozen=True, slots=True)
class AdultReferenceTrajectory:
    """Deterministic synthetic trajectory with no subjective-state claim."""

    initial_state: AdultMaleSexualReferenceState
    events: tuple[AdultReferenceSyntheticEvent, ...]
    states: tuple[AdultMaleSexualReferenceState, ...]
    transitions: tuple[AdultReferenceTransition, ...]
    policy_label: str
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if len(self.states) != len(self.events):
            raise ValueError("states must contain one successor per event")
        if len(self.transitions) != len(self.events):
            raise ValueError("transitions must contain one trace per event")
        _require_nonempty("policy_label", self.policy_label)
        previous_state_id = self.initial_state.state_id
        for state, transition in zip(self.states, self.transitions, strict=True):
            if transition.predecessor_state_id != previous_state_id:
                raise ValueError("transition predecessor does not match state chain")
            if transition.successor_state_id != state.state_id:
                raise ValueError("transition successor does not match state chain")
            if state.subject_ref != self.initial_state.subject_ref:
                raise ValueError("trajectory cannot change subject_ref")
            previous_state_id = state.state_id
        if self.canonical_effect != "NONE":
            raise ValueError("trajectory cannot create canonical effect")
        if self.action_authority != "NONE":
            raise ValueError("trajectory cannot grant action authority")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("trajectory cannot establish phenomenal experience")

    @property
    def final_state(self) -> AdultMaleSexualReferenceState:
        return self.states[-1] if self.states else self.initial_state

    def fingerprint(self) -> str:
        payload = {
            "policy_label": self.policy_label,
            "initial_state": adult_reference_state_payload(self.initial_state),
            "events": [adult_reference_event_payload(event) for event in self.events],
            "states": [adult_reference_state_payload(state) for state in self.states],
            "transitions": [
                adult_reference_transition_payload(item) for item in self.transitions
            ],
        }
        return _digest_payload(payload)


def _combine_onset_context(
    previous: DesireOnsetContext,
    observed: DesireOnsetContext,
) -> DesireOnsetContext:
    if observed is DesireOnsetContext.UNKNOWN:
        return previous
    if previous is DesireOnsetContext.UNKNOWN:
        return observed
    if previous is observed:
        return previous
    return DesireOnsetContext.MIXED


def _step_estimate(
    previous: ReferenceEstimate,
    *,
    channel: str,
    drive: float,
    step_size: float,
    event: AdultReferenceSyntheticEvent,
) -> tuple[ReferenceEstimate, ReferenceChannelTransition]:
    if previous.reference_level is None:
        raise ValueError(
            "simulation requires an explicit numeric seed; UNKNOWN cannot be "
            "silently converted into an adult-male default"
        )
    current = _clamp_unit(previous.reference_level + (step_size * drive))
    current_uncertainty = max(previous.uncertainty, event.uncertainty)
    successor = ReferenceEstimate(
        reference_level=current,
        uncertainty=current_uncertainty,
        source_ref=f"synthetic-event:{event.event_id}",
        context_ref=event.context_ref,
        time_window_ref=event.time_window_ref,
    )
    transition = ReferenceChannelTransition(
        channel=channel,
        previous=previous.reference_level,
        drive=drive,
        step_size=step_size,
        current=current,
        previous_uncertainty=previous.uncertainty,
        event_uncertainty=event.uncertainty,
        current_uncertainty=current_uncertainty,
    )
    return successor, transition



class AdultReferenceSimulationEngine:
    """Deterministic toy transition engine for synthetic research events only."""

    def __init__(
        self,
        policy: AdultReferenceSimulationPolicy = (
            DEFAULT_ADULT_REFERENCE_SIMULATION_POLICY
        ),
    ) -> None:
        self._policy = policy

    def step(
        self,
        state: AdultMaleSexualReferenceState,
        event: AdultReferenceSyntheticEvent,
        *,
        successor_state_id: str,
    ) -> tuple[AdultMaleSexualReferenceState, AdultReferenceTransition]:
        _require_nonempty("successor_state_id", successor_state_id)

        excitation, excitation_trace = _step_estimate(
            state.excitation_reference,
            channel="EXCITATION_REFERENCE",
            drive=event.excitation_drive,
            step_size=self._policy.excitation_step_size,
            event=event,
        )
        inhibition, inhibition_trace = _step_estimate(
            state.inhibition_reference,
            channel="INHIBITION_REFERENCE",
            drive=event.inhibition_drive,
            step_size=self._policy.inhibition_step_size,
            event=event,
        )
        episode, episode_trace = _step_estimate(
            state.episode_state_reference,
            channel="EPISODE_STATE_REFERENCE",
            drive=event.episode_drive,
            step_size=self._policy.episode_step_size,
            event=event,
        )
        disposition, disposition_trace = _step_estimate(
            state.disposition_reference,
            channel="DISPOSITION_REFERENCE",
            drive=event.disposition_observation_drive,
            step_size=self._policy.disposition_step_size,
            event=event,
        )

        onset_context = _combine_onset_context(
            state.desire_onset_context,
            event.onset_context_evidence,
        )
        target_scope = (
            state.target_scope
            if event.target_scope is TargetScope.UNKNOWN
            else event.target_scope
        )
        provenance_refs = tuple(
            dict.fromkeys(
                (
                    *state.provenance_refs,
                    *event.provenance_refs,
                    f"synthetic-event:{event.event_id}",
                )
            )
        )

        successor = AdultMaleSexualReferenceState(
            state_id=successor_state_id,
            subject_ref=state.subject_ref,
            context_ref=event.context_ref,
            desire_onset_context=onset_context,
            excitation_reference=excitation,
            inhibition_reference=inhibition,
            disposition_reference=disposition,
            episode_state_reference=episode,
            target_scope=target_scope,
            provenance_refs=provenance_refs,
        )
        transition = AdultReferenceTransition(
            predecessor_state_id=state.state_id,
            successor_state_id=successor.state_id,
            event_id=event.event_id,
            channels=(
                excitation_trace,
                inhibition_trace,
                disposition_trace,
                episode_trace,
            ),
            previous_onset_context=state.desire_onset_context,
            current_onset_context=onset_context,
            previous_target_scope=state.target_scope,
            current_target_scope=target_scope,
            policy_label=self._policy.policy_label,
        )
        return successor, transition


class AdultReferenceSimulationHarness:
    """Run and replay a bounded synthetic adult-reference trajectory."""

    def run(
        self,
        initial_state: AdultMaleSexualReferenceState,
        events: Iterable[AdultReferenceSyntheticEvent],
        *,
        policy: AdultReferenceSimulationPolicy = (
            DEFAULT_ADULT_REFERENCE_SIMULATION_POLICY
        ),
    ) -> AdultReferenceTrajectory:
        frozen_events = tuple(events)
        engine = AdultReferenceSimulationEngine(policy)
        current = initial_state
        states: list[AdultMaleSexualReferenceState] = []
        transitions: list[AdultReferenceTransition] = []
        for index, event in enumerate(frozen_events, start=1):
            current, transition = engine.step(
                current,
                event,
                successor_state_id=(
                    f"{initial_state.state_id}:{policy.policy_label}:{index}"
                ),
            )
            states.append(current)
            transitions.append(transition)
        return AdultReferenceTrajectory(
            initial_state=initial_state,
            events=frozen_events,
            states=tuple(states),
            transitions=tuple(transitions),
            policy_label=policy.policy_label,
        )

    def replay_matches(
        self,
        trajectory: AdultReferenceTrajectory,
        *,
        policy: AdultReferenceSimulationPolicy = (
            DEFAULT_ADULT_REFERENCE_SIMULATION_POLICY
        ),
    ) -> bool:
        replay = self.run(
            trajectory.initial_state,
            trajectory.events,
            policy=policy,
        )
        return replay.fingerprint() == trajectory.fingerprint()


def reference_estimate_payload(estimate: ReferenceEstimate) -> dict[str, object]:
    return {
        "reference_level": estimate.reference_level,
        "uncertainty": estimate.uncertainty,
        "source_ref": estimate.source_ref,
        "context_ref": estimate.context_ref,
        "time_window_ref": estimate.time_window_ref,
    }


def adult_reference_state_payload(
    state: AdultMaleSexualReferenceState,
) -> dict[str, object]:
    return {
        "schema_version": state.schema_version,
        "state_id": state.state_id,
        "subject_ref": state.subject_ref,
        "context_ref": state.context_ref,
        "desire_onset_context": state.desire_onset_context.value,
        "excitation_reference": reference_estimate_payload(
            state.excitation_reference
        ),
        "inhibition_reference": reference_estimate_payload(
            state.inhibition_reference
        ),
        "disposition_reference": reference_estimate_payload(
            state.disposition_reference
        ),
        "episode_state_reference": reference_estimate_payload(
            state.episode_state_reference
        ),
        "target_scope": state.target_scope.value,
        "provenance_refs": list(state.provenance_refs),
        "runtime_enabled": state.runtime_enabled,
        "automatic_activation": state.automatic_activation,
        "action_authority": state.action_authority,
        "human_consent_inference": state.human_consent_inference,
        "phenomenal_experience_claim": state.phenomenal_experience_claim,
        "subjectivity_claim": state.subjectivity_claim,
        "consciousness_claim": state.consciousness_claim,
        "sexual_function_runtime": state.sexual_function_runtime,
        "intimate_interaction_runtime": state.intimate_interaction_runtime,
        "public_executable_exposure": state.public_executable_exposure,
        "canonical_effect": state.canonical_effect,
    }


def adult_reference_event_payload(
    event: AdultReferenceSyntheticEvent,
) -> dict[str, object]:
    return {
        "schema_version": "ADULT_REFERENCE_SYNTHETIC_EVENT_v0.1.0",
        "event_id": event.event_id,
        "context_ref": event.context_ref,
        "time_window_ref": event.time_window_ref,
        "excitation_drive": event.excitation_drive,
        "inhibition_drive": event.inhibition_drive,
        "episode_drive": event.episode_drive,
        "disposition_observation_drive": event.disposition_observation_drive,
        "onset_context_evidence": event.onset_context_evidence.value,
        "target_scope": event.target_scope.value,
        "uncertainty": event.uncertainty,
        "provenance_refs": list(event.provenance_refs),
        "real_person_target_data": False,
        "human_consent_inference": "FORBIDDEN",
        "action_authority": "NONE",
        "canonical_effect": "NONE",
    }


def adult_reference_transition_payload(
    transition: AdultReferenceTransition,
) -> dict[str, object]:
    return {
        "predecessor_state_id": transition.predecessor_state_id,
        "successor_state_id": transition.successor_state_id,
        "event_id": transition.event_id,
        "channels": [
            {
                "channel": item.channel,
                "previous": item.previous,
                "drive": item.drive,
                "step_size": item.step_size,
                "current": item.current,
                "previous_uncertainty": item.previous_uncertainty,
                "event_uncertainty": item.event_uncertainty,
                "current_uncertainty": item.current_uncertainty,
            }
            for item in transition.channels
        ],
        "previous_onset_context": transition.previous_onset_context.value,
        "current_onset_context": transition.current_onset_context.value,
        "previous_target_scope": transition.previous_target_scope.value,
        "current_target_scope": transition.current_target_scope.value,
        "policy_label": transition.policy_label,
        "human_consent_inferred": transition.human_consent_inferred,
        "action_authorized": transition.action_authorized,
        "phenomenal_experience_claim": transition.phenomenal_experience_claim,
        "canonical_effect": transition.canonical_effect,
    }


def _digest_payload(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def adult_reference_state_digest(
    state: AdultMaleSexualReferenceState,
) -> str:
    return _digest_payload(adult_reference_state_payload(state))


def build_snapshot_receipts(
    trajectory: AdultReferenceTrajectory,
) -> tuple[AdultReferenceSnapshotReceipt, ...]:
    states = (trajectory.initial_state, *trajectory.states)
    receipts: list[AdultReferenceSnapshotReceipt] = []
    previous_receipt = "0" * 64
    for sequence, state in enumerate(states):
        state_digest = adult_reference_state_digest(state)
        receipt_digest = _digest_payload(
            {
                "sequence": sequence,
                "state_id": state.state_id,
                "state_sha256": state_digest,
                "previous_receipt_sha256": previous_receipt,
            }
        )
        receipt = AdultReferenceSnapshotReceipt(
            sequence=sequence,
            state_id=state.state_id,
            state_sha256=state_digest,
            previous_receipt_sha256=previous_receipt,
            receipt_sha256=receipt_digest,
        )
        receipts.append(receipt)
        previous_receipt = receipt_digest
    return tuple(receipts)


def verify_snapshot_receipts(
    trajectory: AdultReferenceTrajectory,
    receipts: tuple[AdultReferenceSnapshotReceipt, ...],
) -> bool:
    return build_snapshot_receipts(trajectory) == receipts
