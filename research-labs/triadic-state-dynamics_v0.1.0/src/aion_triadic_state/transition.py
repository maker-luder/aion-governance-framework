from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from typing import Any

from .canonical import canonical_value
from .models import NormativeState, SelfWorldModel, StateChannel, TriadicStateSnapshot, MotivationalStateView


@dataclass(frozen=True, slots=True)
class TriadicDelta:
    channel: StateChannel
    replacement: MotivationalStateView | SelfWorldModel | NormativeState
    reason: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise ValueError("transition delta requires a reason")


@dataclass(frozen=True, slots=True)
class TriadicTransitionEvent:
    transition_id: str
    sequence: int
    subject_ref: str
    context_ref: str
    from_snapshot_fingerprint: str
    to_snapshot_fingerprint: str
    changed_channel: StateChannel
    event_ref: str
    outcome_ref: str
    correction_ref: str
    provenance_refs: tuple[str, ...]
    delta_reason: str
    previous_event_hash: str
    event_hash: str
    canonical_effect: str = "NONE"
    action_authority: str = "NONE"


@dataclass(frozen=True, slots=True)
class TransitionResult:
    snapshot: TriadicStateSnapshot
    event: TriadicTransitionEvent


def _validate_replacement(snapshot: TriadicStateSnapshot, delta: TriadicDelta) -> None:
    replacement = delta.replacement
    if replacement.subject_ref != snapshot.subject_ref:
        raise ValueError("cross-subject state substitution is forbidden")
    if replacement.context_ref != snapshot.context_ref:
        raise ValueError("cross-context state substitution is forbidden")
    expected: dict[StateChannel, type[Any]] = {
        StateChannel.MOTIVATIONAL_STATE: MotivationalStateView,
        StateChannel.SELF_WORLD_MODEL: SelfWorldModel,
        StateChannel.NORMATIVE_STATE: NormativeState,
    }
    if not isinstance(replacement, expected[delta.channel]):
        raise TypeError("transition replacement does not match declared channel")


def _event_hash(previous_hash: str, payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        {"previous_hash": previous_hash, "payload": canonical_value(payload)},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def apply_transition(
    snapshot: TriadicStateSnapshot,
    delta: TriadicDelta,
    *,
    transition_id: str,
    sequence: int,
    event_ref: str,
    outcome_ref: str,
    correction_ref: str,
    provenance_refs: tuple[str, ...],
    previous_event_hash: str = "GENESIS",
) -> TransitionResult:
    if sequence < 1:
        raise ValueError("transition sequence must be positive")
    if not transition_id.strip() or not event_ref.strip() or not outcome_ref.strip():
        raise ValueError("transition identifiers must not be empty")
    _validate_replacement(snapshot, delta)
    updates: dict[str, Any] = {
        "state_id": f"{snapshot.state_id}:step:{snapshot.logical_step + 1}",
        "logical_step": snapshot.logical_step + 1,
        "predecessor_snapshot_ref": snapshot.fingerprint,
        "evidence_refs": tuple(sorted(set((*snapshot.evidence_refs, *delta.evidence_refs)))),
        "provenance_refs": tuple(sorted(set((*snapshot.provenance_refs, *provenance_refs)))),
    }
    if delta.channel is StateChannel.MOTIVATIONAL_STATE:
        updates["motivational_state"] = delta.replacement
    elif delta.channel is StateChannel.SELF_WORLD_MODEL:
        updates["self_world_model"] = delta.replacement
    else:
        updates["normative_state"] = delta.replacement
    successor = replace(snapshot, **updates)
    payload = {
        "transition_id": transition_id,
        "sequence": sequence,
        "subject_ref": snapshot.subject_ref,
        "context_ref": snapshot.context_ref,
        "from_snapshot_fingerprint": snapshot.fingerprint,
        "to_snapshot_fingerprint": successor.fingerprint,
        "changed_channel": delta.channel.value,
        "event_ref": event_ref,
        "outcome_ref": outcome_ref,
        "correction_ref": correction_ref,
        "provenance_refs": provenance_refs,
        "delta_reason": delta.reason,
        "canonical_effect": "NONE",
        "action_authority": "NONE",
    }
    digest = _event_hash(previous_event_hash, payload)
    event = TriadicTransitionEvent(
        transition_id=transition_id,
        sequence=sequence,
        subject_ref=snapshot.subject_ref,
        context_ref=snapshot.context_ref,
        from_snapshot_fingerprint=snapshot.fingerprint,
        to_snapshot_fingerprint=successor.fingerprint,
        changed_channel=delta.channel,
        event_ref=event_ref,
        outcome_ref=outcome_ref,
        correction_ref=correction_ref,
        provenance_refs=provenance_refs,
        delta_reason=delta.reason,
        previous_event_hash=previous_event_hash,
        event_hash=digest,
    )
    return TransitionResult(successor, event)


def apply_transition_batch(snapshot: TriadicStateSnapshot, deltas: tuple[TriadicDelta, ...], **kwargs: Any) -> TransitionResult:
    if not deltas:
        raise ValueError("at least one delta is required")
    channels = [delta.channel for delta in deltas]
    if len(channels) != len(set(channels)):
        raise ValueError("duplicate or conflicting channel deltas are forbidden")
    if len(deltas) != 1:
        raise ValueError("a transition event must bind exactly one changed channel")
    return apply_transition(snapshot, deltas[0], **kwargs)


def verify_transition_chain(events: tuple[TriadicTransitionEvent, ...]) -> bool:
    previous = "GENESIS"
    expected_sequence = 1
    for event in events:
        if event.sequence != expected_sequence or event.previous_event_hash != previous:
            return False
        payload = {
            "transition_id": event.transition_id,
            "sequence": event.sequence,
            "subject_ref": event.subject_ref,
            "context_ref": event.context_ref,
            "from_snapshot_fingerprint": event.from_snapshot_fingerprint,
            "to_snapshot_fingerprint": event.to_snapshot_fingerprint,
            "changed_channel": event.changed_channel.value,
            "event_ref": event.event_ref,
            "outcome_ref": event.outcome_ref,
            "correction_ref": event.correction_ref,
            "provenance_refs": event.provenance_refs,
            "delta_reason": event.delta_reason,
            "canonical_effect": event.canonical_effect,
            "action_authority": event.action_authority,
        }
        if _event_hash(previous, payload) != event.event_hash:
            return False
        previous = event.event_hash
        expected_sequence += 1
    return True
