from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from .model import MetacognitiveState


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
    """Immutable snapshot of a metacognitive state for restoration."""

    state: MetacognitiveState
    snapshot_id: str
    timestamp: str
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MetacognitiveStateManager:
    """Manage candidate state lifecycle with explicit lineage and ablation trace.

    ``deterministic_seed`` is experiment/provenance metadata. It does not by
    itself make wall-clock timestamps deterministic. Tests that require fully
    reproducible traces should inject ``timestamp_provider``.
    """

    def __init__(
        self,
        deterministic_seed: int | None = None,
        timestamp_provider: Callable[[], str] | None = None,
    ) -> None:
        self._current_state: MetacognitiveState | None = None
        self._history: list[StateTransition] = []
        self._snapshots: dict[str, StateSnapshot] = {}
        self._enabled: bool = True
        self._seed = deterministic_seed
        self._timestamp_provider = timestamp_provider
        self._step_counter = 0

    def initialize(self, state: MetacognitiveState) -> None:
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
        new_state: MetacognitiveState,
        transition_type: str = "UPDATE",
        reason: str = "State update",
    ) -> None:
        if not self._enabled:
            raise RuntimeError("Module is disabled")
        if self._current_state is None:
            raise RuntimeError("No current state; call initialize() first")
        if new_state.subject_ref != self._current_state.subject_ref:
            raise ValueError(
                "subject_ref cannot change through ordinary transition; "
                "use an explicit lineage/migration mechanism"
            )
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

    def get_state(self) -> MetacognitiveState | None:
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
        snap = StateSnapshot(
            state=self._current_state,
            snapshot_id=snapshot_id,
            timestamp=self._timestamp(),
            seed=self._seed,
        )
        self._snapshots[snapshot_id] = snap
        return snap

    def restore(self, snapshot_id: str) -> MetacognitiveState:
        if snapshot_id not in self._snapshots:
            raise KeyError(f"Snapshot {snapshot_id} not found")
        snap = self._snapshots[snapshot_id]
        from_id = self._current_state.state_id if self._current_state is not None else "NULL"
        if self._current_state is not None and snap.state.subject_ref != self._current_state.subject_ref:
            raise ValueError("snapshot subject_ref does not match current subject lineage")
        self._current_state = snap.state
        self._history.append(
            StateTransition(
                from_state_id=from_id,
                to_state_id=snap.state.state_id,
                transition_type="RESTORE",
                timestamp=self._timestamp(),
                reason=f"Restored from snapshot {snapshot_id}",
                deterministic_seed=self._seed,
            )
        )
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

    def ablate(self, capacity: str | None = None) -> None:
        """Ablate a capacity or disable the whole module with explicit trace.

        Removing the final remaining component disables the module instead of
        constructing an invalid empty ``MetacognitiveState``.
        """
        if not self._enabled:
            raise RuntimeError("Module is disabled")

        if capacity is None:
            from_id = self._current_state.state_id if self._current_state is not None else "NULL"
            self._history.append(
                StateTransition(
                    from_state_id=from_id,
                    to_state_id="MODULE_DISABLED",
                    transition_type="ABLATE_MODULE",
                    timestamp=self._timestamp(),
                    reason="Whole metacognitive candidate module ablated",
                    deterministic_seed=self._seed,
                )
            )
            self._enabled = False
            self._step_counter += 1
            return

        if self._current_state is None:
            raise RuntimeError("No current state to ablate")

        old_state = self._current_state
        remaining = tuple(c for c in old_state.components if c.capacity.value != capacity)
        if len(remaining) == len(old_state.components):
            raise KeyError(f"Capacity {capacity} is not active in current state")

        if not remaining:
            self._history.append(
                StateTransition(
                    from_state_id=old_state.state_id,
                    to_state_id="MODULE_DISABLED",
                    transition_type="ABLATE_CAPACITY_DISABLE",
                    timestamp=self._timestamp(),
                    reason=f"Ablating {capacity} removed the final component",
                    deterministic_seed=self._seed,
                )
            )
            self._enabled = False
            self._step_counter += 1
            return

        active_layers = tuple(
            layer
            for layer in old_state.active_layers
            if any(component.layer == layer for component in remaining)
        )
        new_state = MetacognitiveState(
            state_id=f"{old_state.state_id}-ablated-{capacity.lower()}",
            subject_ref=old_state.subject_ref,
            context_ref=old_state.context_ref,
            components=remaining,
            current_depth=old_state.current_depth,
            active_layers=active_layers,
            uncertainty_estimate=old_state.uncertainty_estimate,
            conflict_detected=old_state.conflict_detected,
            canonical_effect=old_state.canonical_effect,
            phenomenal_experience_claim=old_state.phenomenal_experience_claim,
            subjectivity_conclusion=old_state.subjectivity_conclusion,
            continuity_claim=old_state.continuity_claim,
        )
        self.transition(
            new_state,
            transition_type="ABLATE_CAPACITY",
            reason=f"Removed capacity {capacity}",
        )

    def is_enabled(self) -> bool:
        return self._enabled

    def _timestamp(self) -> str:
        if self._timestamp_provider is not None:
            return self._timestamp_provider()
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
