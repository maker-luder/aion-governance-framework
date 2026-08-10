from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .model import LineageState


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
    """Immutable snapshot of a lineage state for restoration."""

    state: LineageState
    snapshot_id: str
    timestamp: str
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LineageStateManager:
    """Manages continuity lineage state lifecycle with reset, snapshot, and restore."""

    def __init__(self, deterministic_seed: int | None = None) -> None:
        self._current_state: LineageState | None = None
        self._history: list[StateTransition] = []
        self._snapshots: dict[str, StateSnapshot] = {}
        self._enabled: bool = True
        self._seed = deterministic_seed
        self._step_counter = 0

    def initialize(self, state: LineageState) -> None:
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
        new_state: LineageState,
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

    def get_state(self) -> LineageState | None:
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

    def restore(self, snapshot_id: str) -> LineageState:
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

    def ablate(self, lineage_type: str | None = None) -> None:
        """Disable specific lineage type or entire module."""
        if lineage_type is None:
            self.disable()
        else:
            if self._current_state is not None:
                from .model import LineageState, LineageType, LineageConfig
                try:
                    lt = LineageType(lineage_type)
                except ValueError:
                    return
                new_nodes = tuple(n for n in self._current_state.nodes if n.lineage_type != lt)
                if len(new_nodes) != len(self._current_state.nodes):
                    old = self._current_state
                    new_tracked = tuple(t for t in old.config.tracked_types if t != lt)
                    new_config = LineageConfig(
                        config_id=f"{old.config.config_id}-ablated",
                        agent_id=old.config.agent_id,
                        tracked_types=new_tracked,
                        max_depth=old.config.max_depth,
                        strength_threshold=old.config.strength_threshold,
                    )
                    # Recalculate overall_continuity and branch_count
                    new_overall = sum(n.continuity_strength for n in new_nodes) / len(new_nodes) if new_nodes else 0.0
                    new_branches = len(set(n.node_id for n in new_nodes if len(self._get_children_new(new_nodes, n.node_id)) > 1))
                    new_heads = tuple(n.node_id for n in new_nodes if not self._get_children_new(new_nodes, n.node_id))
                    self._current_state = LineageState(
                        state_id=f"{old.state_id}-ablated",
                        config=new_config,
                        nodes=new_nodes,
                        root_node_id=old.root_node_id if old.root_node_id and any(n.node_id == old.root_node_id for n in new_nodes) else None,
                        current_head_ids=new_heads,
                        overall_continuity=new_overall,
                        branch_count=new_branches,
                        events=old.events,
                    )

    def _get_children_new(self, nodes: tuple, node_id: str) -> tuple:
        return tuple(n for n in nodes if node_id in n.parent_ids)

    def is_enabled(self) -> bool:
        return self._enabled

    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"