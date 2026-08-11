from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class SessionItem:
    sequence: int
    kind: str
    role: str
    content: str
    source_ref: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PendingInterrupt:
    interrupt_id: str
    call_id: str
    tool_name: str
    arguments: Mapping[str, Any]
    reason: str


@dataclass(frozen=True)
class SessionSnapshot:
    session_id: str
    revision: int
    items: tuple[SessionItem, ...]
    pending_interrupts: tuple[PendingInterrupt, ...]
    canonical_effect: str = "NONE"

    def to_json(self) -> str:
        return json.dumps({"session_id": self.session_id, "revision": self.revision, "items": [asdict(item) for item in self.items], "pending_interrupts": [asdict(item) for item in self.pending_interrupts], "canonical_effect": self.canonical_effect}, ensure_ascii=False, sort_keys=True)


class SessionContextManager:
    """Short-lived working-context state. This is not AION long-term memory."""

    def __init__(self, session_id: str) -> None:
        if not session_id.strip():
            raise ValueError("session_id must be non-empty")
        self.session_id = session_id
        self._items: list[SessionItem] = []
        self._pending: dict[str, PendingInterrupt] = {}
        self._revision = 0

    @property
    def revision(self) -> int:
        return self._revision

    def append(self, *, kind: str, role: str, content: str, source_ref: str | None = None, metadata: Mapping[str, Any] | None = None) -> SessionItem:
        if not kind.strip() or not role.strip():
            raise ValueError("kind and role must be non-empty")
        item = SessionItem(sequence=len(self._items) + 1, kind=kind, role=role, content=content, source_ref=source_ref, metadata=dict(metadata or {}))
        self._items.append(item)
        self._revision += 1
        return item

    def add_interrupt(self, *, interrupt_id: str, call_id: str, tool_name: str, arguments: Mapping[str, Any], reason: str) -> PendingInterrupt:
        if interrupt_id in self._pending:
            raise ValueError("duplicate interrupt_id")
        interrupt = PendingInterrupt(interrupt_id, call_id, tool_name, dict(arguments), reason)
        self._pending[interrupt_id] = interrupt
        self._revision += 1
        return interrupt

    def resolve_interrupt(self, interrupt_id: str) -> PendingInterrupt:
        try:
            interrupt = self._pending.pop(interrupt_id)
        except KeyError as exc:
            raise KeyError(f"unknown interrupt_id: {interrupt_id}") from exc
        self._revision += 1
        return interrupt

    def get_interrupt(self, interrupt_id: str) -> PendingInterrupt:
        try:
            return self._pending[interrupt_id]
        except KeyError as exc:
            raise KeyError(f"unknown interrupt_id: {interrupt_id}") from exc

    def assemble_messages(self, *, max_chars: int = 32_000, memory_projection: Iterable[Mapping[str, Any]] = ()) -> tuple[Mapping[str, Any], ...]:
        if max_chars <= 0:
            raise ValueError("max_chars must be positive")
        projection = [{"role": "system", "content": str(item.get("content", "")), "memory_id": item.get("memory_id"), "source_ref": item.get("source_ref"), "authority": "EXTERNAL_GOVERNED_MEMORY_PROJECTION"} for item in memory_projection]
        history: list[Mapping[str, Any]] = [{"role": item.role, "content": item.content, "kind": item.kind, "sequence": item.sequence} for item in self._items if item.kind in {"message", "tool_result", "runtime_note"}]
        combined = projection + history
        selected: list[Mapping[str, Any]] = []
        used = 0
        for item in reversed(combined):
            size = len(str(item.get("content", "")))
            if selected and used + size > max_chars:
                break
            if size > max_chars and not selected:
                clipped = dict(item)
                clipped["content"] = str(item.get("content", ""))[-max_chars:]
                selected.append(clipped)
                break
            selected.append(item)
            used += size
        selected.reverse()
        return tuple(selected)

    def snapshot(self) -> SessionSnapshot:
        return SessionSnapshot(session_id=self.session_id, revision=self._revision, items=tuple(self._items), pending_interrupts=tuple(self._pending.values()))
