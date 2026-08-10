from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from .model import BoundaryConfiguration, BoundaryState, SelfOtherDistinction


@dataclass(frozen=True, slots=True)
class StateTransition:
    """Records state and subject-transition provenance."""

    from_state_id: str
    to_state_id: str
    transition_type: str
    timestamp: str
    reason: str
    from_subject_ref: str | None = None
    to_subject_ref: str | None = None
    deterministic_seed: int | None = None


@dataclass(frozen=True, slots=True)
class StateSnapshot:
    """Immutable snapshot of a boundary state for restoration."""

    state: BoundaryState
    snapshot_id: str
    timestamp: str
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BoundaryStateManager:
    """Manage boundary-state lifecycle with explicit subject and ablation trace."""

    EXPLICIT_SUBJECT_TRANSITIONS = frozenset({
        "SUBJECT_SWITCH", "PERSPECTIVE_SWITCH", "CONTEXT_REBIND", "HANDOFF", "IDENTITY_ROLE_SWITCH"
    })

    def __init__(self, deterministic_seed: int | None = None, timestamp_provider: Callable[[], str] | None = None) -> None:
        self._current_state: BoundaryState | None = None
        self._history: list[StateTransition] = []
        self._snapshots: dict[str, StateSnapshot] = {}
        self._enabled = True
        self._seed = deterministic_seed
        self._timestamp_provider = timestamp_provider
        self._step_counter = 0

    def initialize(self, state: BoundaryState) -> None:
        if not self._enabled:
            raise RuntimeError("Module is disabled")
        self._current_state = state
        self._history.append(StateTransition("NULL", state.state_id, "INITIALIZE", self._timestamp(), "Initial state creation", None, state.subject_ref, self._seed))

    def transition(self, new_state: BoundaryState, transition_type: str = "UPDATE", reason: str = "State update") -> None:
        if not self._enabled:
            raise RuntimeError("Module is disabled")
        if self._current_state is None:
            raise RuntimeError("No current state; call initialize() first")
        if not transition_type.strip() or not reason.strip():
            raise ValueError("transition_type and reason must be non-empty")
        old = self._current_state
        if new_state.subject_ref != old.subject_ref and transition_type not in self.EXPLICIT_SUBJECT_TRANSITIONS:
            raise ValueError("subject_ref change requires an explicit subject-transition type")
        self._history.append(StateTransition(old.state_id, new_state.state_id, transition_type, self._timestamp(), reason, old.subject_ref, new_state.subject_ref, self._seed))
        self._current_state = new_state
        self._step_counter += 1

    def get_state(self) -> BoundaryState | None:
        return self._current_state

    def reset(self) -> None:
        self._current_state = None
        self._history.clear()
        self._snapshots.clear()
        self._step_counter = 0

    def snapshot(self, snapshot_id: str | None = None) -> StateSnapshot:
        if self._current_state is None:
            raise RuntimeError("No current state to snapshot")
        if snapshot_id is None:
            snapshot_id = f"snap-{self._step_counter}-{self._timestamp()}"
        if not snapshot_id.strip():
            raise ValueError("snapshot_id must be non-empty")
        snap = StateSnapshot(self._current_state, snapshot_id, self._timestamp(), self._seed)
        self._snapshots[snapshot_id] = snap
        return snap

    def restore(self, snapshot_id: str, *, allow_subject_switch: bool = False) -> BoundaryState:
        if snapshot_id not in self._snapshots:
            raise KeyError(f"Snapshot {snapshot_id} not found")
        snap = self._snapshots[snapshot_id]
        old = self._current_state
        subject_changed = old is not None and snap.state.subject_ref != old.subject_ref
        if subject_changed and not allow_subject_switch:
            raise ValueError("snapshot belongs to a different subject; explicit subject-switch restore required")
        self._current_state = snap.state
        self._history.append(StateTransition(
            old.state_id if old is not None else "NULL",
            snap.state.state_id,
            "RESTORE_SUBJECT_SWITCH" if subject_changed else "RESTORE",
            self._timestamp(),
            f"Restored from snapshot {snapshot_id}",
            old.subject_ref if old is not None else None,
            snap.state.subject_ref,
            self._seed,
        ))
        self._step_counter += 1
        return snap.state

    def list_snapshots(self) -> tuple[str, ...]:
        return tuple(self._snapshots.keys())

    def get_history(self) -> tuple[StateTransition, ...]:
        return tuple(self._history)

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def ablate(self, distinction: str | None = None) -> None:
        if not self._enabled:
            raise RuntimeError("Module is disabled")
        old = self._current_state
        if distinction is None:
            self._history.append(StateTransition(
                old.state_id if old is not None else "NULL", "MODULE_DISABLED", "ABLATE_MODULE",
                self._timestamp(), "Whole self-other boundary candidate module ablated",
                old.subject_ref if old is not None else None, old.subject_ref if old is not None else None, self._seed,
            ))
            self._enabled = False
            self._step_counter += 1
            return
        if old is None:
            raise RuntimeError("No current state to ablate")
        try:
            dist_type = SelfOtherDistinction(distinction)
        except ValueError as exc:
            raise KeyError(f"Unknown distinction {distinction}") from exc
        if dist_type not in old.active_distinctions:
            raise KeyError(f"Distinction {distinction} is not active in current state")
        new_distinctions = tuple(d for d in old.active_distinctions if d != dist_type)
        if not new_distinctions:
            self._history.append(StateTransition(old.state_id, "MODULE_DISABLED", "ABLATE_DISTINCTION_DISABLE", self._timestamp(), f"Ablating {distinction} removed the final active distinction", old.subject_ref, old.subject_ref, self._seed))
            self._enabled = False
            self._step_counter += 1
            return
        new_weights = {k: v for k, v in old.config.distinction_weights.items() if k != dist_type}
        total = sum(new_weights.values())
        new_weights = {k: v / total for k, v in new_weights.items()}
        new_config = BoundaryConfiguration(
            config_id=f"{old.config.config_id}-ablated-{distinction.lower()}",
            default_mode=old.config.default_mode,
            distinction_weights=new_weights,
            permeability_threshold=old.config.permeability_threshold,
            rigidity_threshold=old.config.rigidity_threshold,
            canonical_effect=old.config.canonical_effect,
            empathy_claim=old.config.empathy_claim,
        )
        new_state = BoundaryState(
            state_id=f"{old.state_id}-ablated-{distinction.lower()}",
            subject_ref=old.subject_ref,
            config=new_config,
            current_mode=old.current_mode,
            active_distinctions=new_distinctions,
            other_models=old.other_models,
            boundary_permeability=old.boundary_permeability,
            confusion_index=old.confusion_index,
            recent_events=old.recent_events,
            canonical_effect=old.canonical_effect,
            empathy_claim=old.empathy_claim,
            theory_of_mind_claim=old.theory_of_mind_claim,
            shared_subjectivity_claim=old.shared_subjectivity_claim,
        )
        self.transition(new_state, transition_type="ABLATE_DISTINCTION", reason=f"Removed distinction {distinction}")

    def is_enabled(self) -> bool:
        return self._enabled

    def _timestamp(self) -> str:
        if self._timestamp_provider is not None:
            return self._timestamp_provider()
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
