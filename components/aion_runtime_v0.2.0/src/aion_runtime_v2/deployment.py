from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from typing import Any


class DeploymentEventType(str, Enum):
    INSTALL = "INSTALL"
    FIRST_INSTANTIATION = "FIRST_INSTANTIATION"
    RESTART = "RESTART"
    RESTORE = "RESTORE"
    MIGRATE = "MIGRATE"
    CLONE = "CLONE"
    FORK = "FORK"
    ROLLBACK = "ROLLBACK"
    UPGRADE = "UPGRADE"
    RETIRE = "RETIRE"


@dataclass(frozen=True)
class DeploymentEvent:
    sequence: int
    event_type: DeploymentEventType
    deployment_id: str
    runtime_instance_id: str
    lineage_id: str
    parent_event_hash: str | None
    source_checkpoint_id: str | None = None
    source_lineage_id: str | None = None
    metadata: dict[str, Any] | None = None
    canonical_effect: str = "NONE"

    def digest(self) -> str:
        payload = json.dumps(asdict(self), ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


class DeploymentLedger:
    def __init__(self) -> None:
        self._events: list[DeploymentEvent] = []

    def append(self, *, event_type: DeploymentEventType, deployment_id: str, runtime_instance_id: str, lineage_id: str, source_checkpoint_id: str | None = None, source_lineage_id: str | None = None, metadata: dict[str, Any] | None = None) -> DeploymentEvent:
        if not all(value.strip() for value in (deployment_id, runtime_instance_id, lineage_id)):
            raise ValueError("deployment/runtime/lineage identifiers must be non-empty")
        if event_type in {DeploymentEventType.RESTORE, DeploymentEventType.ROLLBACK, DeploymentEventType.CLONE, DeploymentEventType.FORK} and not source_checkpoint_id:
            raise ValueError(f"{event_type.value} requires source_checkpoint_id")
        if event_type in {DeploymentEventType.CLONE, DeploymentEventType.FORK}:
            if not source_lineage_id:
                raise ValueError(f"{event_type.value} requires source_lineage_id")
            if source_lineage_id == lineage_id:
                raise ValueError(f"{event_type.value} must create a distinct lineage_id")
        previous = self._events[-1] if self._events else None
        parent_hash = previous.digest() if previous else None
        event = DeploymentEvent(sequence=len(self._events) + 1, event_type=event_type, deployment_id=deployment_id, runtime_instance_id=runtime_instance_id, lineage_id=lineage_id, parent_event_hash=parent_hash, source_checkpoint_id=source_checkpoint_id, source_lineage_id=source_lineage_id, metadata=dict(metadata or {}))
        self._events.append(event)
        return event

    def verify_chain(self) -> bool:
        previous_hash: str | None = None
        for event in self._events:
            if event.parent_event_hash != previous_hash:
                return False
            previous_hash = event.digest()
        return True

    def events(self) -> tuple[DeploymentEvent, ...]:
        return tuple(self._events)
