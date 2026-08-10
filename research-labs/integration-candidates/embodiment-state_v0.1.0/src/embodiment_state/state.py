from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .model import EmbodimentState


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
    """Immutable snapshot of an embodiment state for restoration."""

    state: EmbodimentState
    snapshot_id: str
    timestamp: str
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EmbodimentStateManager:
    """Manages embodiment state lifecycle with reset, snapshot, and restore."""

    def __init__(self, deterministic_seed: int | None = None) -> None:
        self._current_state: EmbodimentState | None = None
        self._history: list[StateTransition] = []
        self._snapshots: dict[str, StateSnapshot] = {}
        self._enabled: bool = True
        self._seed = deterministic_seed
        self._step_counter = 0

    def initialize(self, state: EmbodimentState) -> None:
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
        new_state: EmbodimentState,
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

    def get_state(self) -> EmbodimentState | None:
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

    def restore(self, snapshot_id: str) -> EmbodimentState:
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

    def ablate(self, modality: str | None = None) -> None:
        """Disable specific modality or entire module."""
        if modality is None:
            self.disable()
        else:
            if self._current_state is not None:
                from .model import EmbodimentState, ModalityConfig, ModalityType
                try:
                    mod_type = ModalityType(modality)
                except ValueError:
                    return
                new_modalities = tuple(
                    m for m in self._current_state.config.modalities if m.modality != mod_type
                )
                if len(new_modalities) != len(self._current_state.config.modalities):
                    new_config = EmbodimentState.__dataclass_fields__["config"].default  # type: ignore
                    # Reconstruct config with filtered modalities
                    old_config = self._current_state.config
                    from .model import EmbodimentConfig
                    new_config_obj = EmbodimentConfig(
                        config_id=f"{old_config.config_id}-ablated",
                        agent_id=old_config.agent_id,
                        template_ref=old_config.template_ref,
                        modalities=new_modalities,
                        joint_count=old_config.joint_count,
                    )
                    self._current_state = EmbodimentState(
                        state_id=f"{self._current_state.state_id}-ablated",
                        config=new_config_obj,
                        status=self._current_state.status,
                        proprioceptive_signals=self._current_state.proprioceptive_signals,
                        interoceptive_signals=self._current_state.interoceptive_signals,
                        motor_commands=self._current_state.motor_commands,
                        uncertainty_estimate=self._current_state.uncertainty_estimate,
                    )

    def is_enabled(self) -> bool:
        return self._enabled

    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"