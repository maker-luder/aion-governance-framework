"""Hash-chained durable execution evidence for the shared substrate."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .models import SubstrateError, canonical_json_bytes, sha256_json

EVENT_LOG_FILENAME = "substrate_execution_events.jsonl"
EXECUTION_EVIDENCE_FILENAME = "substrate_execution_evidence.json"


@dataclass(frozen=True, slots=True)
class DurableLogSummary:
    path: Path
    sha256: str
    event_count: int
    head_event_sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path.name,
            "sha256": self.sha256,
            "event_count": self.event_count,
            "head_event_sha256": self.head_event_sha256,
        }


def _event_record(
    *,
    sequence: int,
    event_type: str,
    facts: Mapping[str, Any],
    previous_event_sha256: str | None,
) -> dict[str, Any]:
    if sequence < 1:
        raise SubstrateError("durable event sequence must be positive")
    if not event_type.strip():
        raise SubstrateError("durable event type is required")
    core = {
        "sequence": sequence,
        "event_type": event_type,
        "facts": dict(facts),
        "previous_event_sha256": previous_event_sha256,
    }
    return {**core, "event_sha256": sha256_json(core)}


def persist_execution_event_log(
    output_root: Path,
    events: Sequence[tuple[str, Mapping[str, Any]]],
) -> DurableLogSummary:
    """Persist deterministic, content-minimized, hash-chained execution events."""

    if not output_root.is_dir():
        raise SubstrateError("output_root is unavailable for durable execution events")
    if not events:
        raise SubstrateError("at least one durable execution event is required")

    previous: str | None = None
    records: list[dict[str, Any]] = []
    for sequence, (event_type, facts) in enumerate(events, start=1):
        record = _event_record(
            sequence=sequence,
            event_type=event_type,
            facts=facts,
            previous_event_sha256=previous,
        )
        records.append(record)
        previous = str(record["event_sha256"])

    payload = b"".join(canonical_json_bytes(record) + b"\n" for record in records)
    path = output_root / EVENT_LOG_FILENAME
    try:
        path.write_bytes(payload)
    except OSError as exc:
        raise SubstrateError("durable execution event log could not be persisted") from exc

    summary = verify_execution_event_log(path)
    if summary.event_count != len(records):
        raise SubstrateError("durable execution event count changed after persistence")
    return summary


def verify_execution_event_log(path: Path) -> DurableLogSummary:
    """Verify sequence, hash-chain linkage, per-event hashes, and file digest."""

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SubstrateError("durable execution event log is unreadable") from exc

    lines = raw.splitlines()
    if not lines:
        raise SubstrateError("durable execution event log is empty")

    previous: str | None = None
    head = ""
    for expected_sequence, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SubstrateError("durable execution event log contains invalid JSON") from exc
        if not isinstance(record, dict):
            raise SubstrateError("durable execution event must be an object")
        if record.get("sequence") != expected_sequence:
            raise SubstrateError("durable execution event sequence is invalid")
        if record.get("previous_event_sha256") != previous:
            raise SubstrateError("durable execution event hash chain is broken")
        event_sha = str(record.get("event_sha256", ""))
        core = {key: value for key, value in record.items() if key != "event_sha256"}
        if len(event_sha) != 64 or sha256_json(core) != event_sha:
            raise SubstrateError("durable execution event digest is invalid")
        previous = event_sha
        head = event_sha

    return DurableLogSummary(
        path=path,
        sha256=hashlib.sha256(raw).hexdigest(),
        event_count=len(lines),
        head_event_sha256=head,
    )


def persist_execution_evidence(
    output_root: Path,
    *,
    binding: Mapping[str, Any],
    adapter: Mapping[str, Any],
    registry_snapshot_sha256: str,
    policy_decision_sha256: str,
    request_sha256: str,
    runtime_audit_sha256: str,
    runtime_result_sha256: str,
    trajectory_sha256: str,
    event_log: DurableLogSummary,
    receipt_filename: str,
) -> tuple[Path, str]:
    """Persist a non-canonical evidence envelope for one admitted execution."""

    envelope = {
        "schema_version": "0.1.0",
        "record_type": "AION_ASTRA_SUBSTRATE_EXECUTION_EVIDENCE",
        "binding": dict(binding),
        "adapter": dict(adapter),
        "registry_snapshot_sha256": registry_snapshot_sha256,
        "policy_decision_sha256": policy_decision_sha256,
        "request_sha256": request_sha256,
        "runtime_audit_sha256": runtime_audit_sha256,
        "runtime_result_sha256": runtime_result_sha256,
        "trajectory_sha256": trajectory_sha256,
        "durable_event_log": event_log.to_dict(),
        "execution_receipt": {
            "path": receipt_filename,
            "sha256_binding": "RECORDED_IN_EXECUTION_RECEIPT",
        },
        "boundaries": {
            "canonical_effect": "NONE",
            "deployment": False,
            "network_access": False,
            "live_dsh_execution": False,
            "research_record": False,
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "independent_ivv": "NOT_ACHIEVED",
        },
    }
    payload = canonical_json_bytes(envelope) + b"\n"
    path = output_root / EXECUTION_EVIDENCE_FILENAME
    try:
        path.write_bytes(payload)
    except OSError as exc:
        raise SubstrateError("substrate execution evidence could not be persisted") from exc
    return path, hashlib.sha256(payload).hexdigest()


def verify_execution_evidence(path: Path) -> bool:
    """Verify the event log and the receipt-to-evidence digest closure."""

    try:
        raw = path.read_bytes()
        envelope = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise SubstrateError("substrate execution evidence is unreadable") from exc
    if not isinstance(envelope, dict):
        raise SubstrateError("substrate execution evidence must be an object")
    if envelope.get("record_type") != "AION_ASTRA_SUBSTRATE_EXECUTION_EVIDENCE":
        raise SubstrateError("unexpected substrate execution evidence record type")

    event_log = envelope.get("durable_event_log")
    receipt_ref = envelope.get("execution_receipt")
    if not isinstance(event_log, dict) or not isinstance(receipt_ref, dict):
        raise SubstrateError("substrate execution evidence references are missing")

    event_log_path = path.parent / str(event_log.get("path", ""))
    summary = verify_execution_event_log(event_log_path)
    if summary.sha256 != str(event_log.get("sha256", "")):
        raise SubstrateError("substrate execution event log digest does not match evidence")
    if summary.head_event_sha256 != str(event_log.get("head_event_sha256", "")):
        raise SubstrateError("substrate execution event head does not match evidence")
    if summary.event_count != event_log.get("event_count"):
        raise SubstrateError("substrate execution event count does not match evidence")

    receipt_path = path.parent / str(receipt_ref.get("path", ""))
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SubstrateError("substrate execution receipt is unreadable") from exc
    if not isinstance(receipt, dict):
        raise SubstrateError("substrate execution receipt must be an object")
    evidence_ref = receipt.get("evidence_envelope")
    if not isinstance(evidence_ref, dict):
        raise SubstrateError("substrate execution receipt lacks evidence binding")
    if str(evidence_ref.get("path", "")) != path.name:
        raise SubstrateError("substrate execution receipt points to a different evidence file")
    if str(evidence_ref.get("sha256", "")) != hashlib.sha256(raw).hexdigest():
        raise SubstrateError("substrate execution evidence digest does not match receipt")
    receipt_event_log = receipt.get("durable_event_log")
    if not isinstance(receipt_event_log, dict):
        raise SubstrateError("substrate execution receipt lacks durable event binding")
    if str(receipt_event_log.get("sha256", "")) != summary.sha256:
        raise SubstrateError("receipt and evidence disagree on durable event log digest")
    return True
