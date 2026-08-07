"""Astra-only provenance adapter; never writes to AION streams."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .errors import EpisodicAdapterError
from .interfaces import EpisodicEventWriter


class EpisodicCoreAdapter:
    def __init__(self, writer: EpisodicEventWriter) -> None:
        self.writer = writer

    def record(
        self,
        *,
        task_id: str,
        event_kind: str,
        source_type: str,
        payload: dict[str, Any],
    ) -> str:
        memory_stream = f"ASTRA_MEMORY_{task_id}"
        audit_stream = f"ASTRA_AUDIT_{task_id}"
        if not memory_stream.startswith("ASTRA_") or not audit_stream.startswith("ASTRA_"):
            raise EpisodicAdapterError("Astra stream scope is invalid")
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        try:
            return self.writer.append(
                agent_id="AGENT_ASTRA",
                memory_stream_id=memory_stream,
                audit_stream_id=audit_stream,
                source_type=source_type,
                event_kind=event_kind,
                payload_hash=digest,
            )
        except Exception as exc:
            raise EpisodicAdapterError("provenance recording failed; operation stopped") from exc

    @staticmethod
    def validate_stream(memory_stream_id: str, audit_stream_id: str) -> None:
        if (
            not memory_stream_id.startswith("ASTRA_")
            or not audit_stream_id.startswith("ASTRA_")
            or memory_stream_id.startswith("AION_")
            or audit_stream_id.startswith("AION_")
        ):
            raise EpisodicAdapterError("AION or non-Astra stream write rejected")
