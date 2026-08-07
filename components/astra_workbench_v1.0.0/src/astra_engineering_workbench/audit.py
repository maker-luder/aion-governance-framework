"""Append-only JSONL audit with deterministic hash-chain verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .errors import AuditError


def _canonical(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class AppendOnlyAudit:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _records(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            return [
                json.loads(line)
                for line in self.path.read_text(encoding="utf-8").splitlines()
                if line
            ]
        except (OSError, json.JSONDecodeError) as exc:
            raise AuditError("audit log is unreadable") from exc

    def append(
        self,
        *,
        occurred_at: str,
        task_id: str,
        action: str,
        details: dict[str, Any],
    ) -> str:
        records = self._records()
        if records and not self.verify():
            raise AuditError("audit chain verification failed before append")
        previous_hash = "" if not records else str(records[-1]["event_hash"])
        payload: dict[str, Any] = {
            "sequence": len(records) + 1,
            "occurred_at": occurred_at,
            "task_id": task_id,
            "action": action,
            "details": details,
            "previous_hash": previous_hash,
        }
        event_hash = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
        payload["event_hash"] = event_hash
        try:
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(_canonical(payload) + "\n")
        except OSError as exc:
            raise AuditError("audit append failed") from exc
        return event_hash

    def verify(self) -> bool:
        previous_hash = ""
        for sequence, record in enumerate(self._records(), start=1):
            if record.get("sequence") != sequence or record.get("previous_hash") != previous_hash:
                return False
            event_hash = str(record.get("event_hash", ""))
            payload = {key: value for key, value in record.items() if key != "event_hash"}
            expected = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
            if event_hash != expected:
                return False
            previous_hash = event_hash
        return True

    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._records())
