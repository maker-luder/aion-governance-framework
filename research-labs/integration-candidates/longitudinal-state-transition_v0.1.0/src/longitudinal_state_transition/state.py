from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .model import LongitudinalState


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
    """Immutable snapshot of a longitudinal state for restoration."""

    state: LongitudinalState
    snapshot_id: str
    timestamp: str
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LongitudinalStateManager:
    """Manages longitudinal state lifecycle with reset, snapshot, and restore."""

    def __init__(self, deterministic_seed: int | None = None) -> None:
        self._current_state: LongitudinalState | None = None
        self._history: list[StateTransition] = []
        self._snapshots: dict[str, StateSnapshot] = {}
        self._enabled: bool = True
        self._seed = deterministic_seed
        self._step_counter = 0

    def initialize(self, state: LongitudinalState) -> None:
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
        new_state: LongitudinalState,
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

    def get_state(self) -> LongitudinalState | None:
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

    def restore(self, snapshot_id: str) -> LongitudinalState:
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

    def ablate(self, dimension: str | None = None) -> None:
        """Remove tracked dimension or disable entire module."""
        if dimension is None:
            self.disable()
        else:
            if self._current_state is not None:
                old = self._current_state
                if dimension in old.config.tracked_dimensions:
                    new_dimensions = tuple(d for d in old.config.tracked_dimensions if d != dimension)
                    if new_dimensions:
                        from .model import LongitudinalConfig, LongitudinalState
                        new_config = LongitudinalConfig(
                            config_id=f"{old.config.config_id}-ablated",
                            subject_ref=old.config.subject_ref,
                            tracked_dimensions=new_dimensions,
                            window_size=old.config.window_size,
                            sensitivity_threshold=old.config.sensitivity_threshold,
                        )
                        new_values = {k: v for k, v in old.dimension_values.items() if k != dimension}
                        new_history = tuple({k: v for k, v in h.items() if k != dimension} for h in old.trajectory_history)
                        self._current_state = LongitudinalState(
                            state_id=f"{old.state_id}-ablated",
                            config=new_config,
                            current_signature=f"{old.current_signature}-ablated",
                            dimension_values=new_values,
                            trajectory_history=new_history,
                            transition_events=old.transition_events,
                            stability_index=old.stability_index,
                            trend_direction=old.trend_direction,
                        )
                    else:
                        self.disable()

    def is_enabled(self) -> bool:
        return self._enabled

    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"