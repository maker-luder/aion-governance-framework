from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .model import BoundaryState


@dataclass(frozen=True, slots=True)
class StateTransition:
    """Records a state transition for traceability."""

    from_state_id: str
    to_state_id: str
    transition_type: str
    timestamp: str
    reason: str
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
    """Manages self-other boundary state lifecycle with reset, snapshot, and restore."""

    def __init__(self, deterministic_seed: int | None = None) -> None:
        self._current_state: BoundaryState | None = None
        self._history: list[StateTransition] = []
        self._snapshots: dict[str, StateSnapshot] = {}
        self._enabled: bool = True
        self._seed = deterministic_seed
        self._step_counter = 0

    def initialize(self, state: BoundaryState) -> None:
        if not self._enabled:
            raise RuntimeError("Module is disabled")
        self._current_state = state
        self._history.append(
            StateTransition(
                from_state_id="NULL",
                to_state_id=state.state_id,
                transition_type="INITIALIZE",
                timestamp=self._timestamp(),
                reason="Initial state creation",
                deterministic_seed=self._seed,
            )
        )

    def transition(
        self,
        new_state: BoundaryState,
        transition_type: str = "UPDATE",
        reason: str = "State update",
    ) -> None:
        if not self._enabled:
            raise RuntimeError("Module is disabled")
        if self._current_state is None:
            raise RuntimeError("No current state; call initialize() first")
        from_id = self._current_state.state_id
        self._history.append(
            StateTransition(
                from_state_id=from_id,
                to_state_id=new_state.state_id,
                transition_type=transition_type,
                timestamp=self._timestamp(),
                reason=reason,
                deterministic_seed=self._seed,
            )
        )
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
        snap = StateSnapshot(
            state=self._current_state,
            snapshot_id=snapshot_id,
            timestamp=self._timestamp(),
            seed=self._seed,
        )
        self._snapshots[snapshot_id] = snap
        return snap

    def restore(self, snapshot_id: str) -> BoundaryState:
        if snapshot_id not in self._snapshots:
            raise KeyError(f"Snapshot {snapshot_id} not found")
        snap = self._snapshots[snapshot_id]
        self._current_state = snap.state
        self._history.append(
            StateTransition(
                from_state_id="RESTORED",
                to_state_id=snap.state.state_id,
                transition_type="RESTORE",
                timestamp=self._timestamp(),
                reason=f"Restored from snapshot {snapshot_id}",
                deterministic_seed=self._seed,
            )
        )
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
        """Disable specific distinction mechanism or entire module."""
        if distinction is None:
            self.disable()
        else:
            if self._current_state is not None:
                from .model import BoundaryState, SelfOtherDistinction
                try:
                    dist_type = SelfOtherDistinction(distinction)
                except ValueError:
                    return
                new_distinctions = tuple(
                    d for d in self._current_state.active_distinctions if d != dist_type
                )
                if len(new_distinctions) != len(self._current_state.active_distinctions):
                    # Rebuild state with filtered distinctions
                    old = self._current_state
                    new_weights = {k: v for k, v in old.config.distinction_weights.items() if k != dist_type}
                    # Renormalize weights
                    total = sum(new_weights.values())
                    if total > 0:
                        new_weights = {k: v / total for k, v in new_weights.items()}
                    from .model import BoundaryConfiguration
                    new_config = BoundaryConfiguration(
                        config_id=f"{old.config.config_id}-ablated",
                        default_mode=old.config.default_mode,
                        distinction_weights=new_weights,
                        permeability_threshold=old.config.permeability_threshold,
                        rigidity_threshold=old.config.rigidity_threshold,
                    )
                    self._current_state = BoundaryState(
                        state_id=f"{old.state_id}-ablated",
                        subject_ref=old.subject_ref,
                        config=new_config,
                        current_mode=old.current_mode,
                        active_distinctions=new_distinctions,
                        other_models=old.other_models,
                        boundary_permeability=old.boundary_permeability,
                        confusion_index=old.confusion_index,
                        recent_events=old.recent_events,
                    )

    def is_enabled(self) -> bool:
        return self._enabled

    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"