from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping, Sequence


class EventState(str, Enum):
    START = "START"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"


class AuditStatus(str, Enum):
    VALID = "VALID"
    HOLD = "HOLD"
    INVALID = "INVALID"


_SECRET_MARKERS = (
    "secret",
    "token",
    "password",
    "passwd",
    "api_key",
    "apikey",
    "authorization",
    "credential",
)


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _valid_digest(digest: str) -> bool:
    return len(digest) == 64 and all(char in "0123456789abcdef" for char in digest.casefold())


def redact_environment(environment: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in environment.items():
        if any(marker in key.casefold() for marker in _SECRET_MARKERS):
            result[key] = "[REDACTED]"
        else:
            result[key] = value
    return result


def environment_is_redacted(environment: Mapping[str, Any]) -> bool:
    for key, value in environment.items():
        if any(marker in key.casefold() for marker in _SECRET_MARKERS) and value != "[REDACTED]":
            return False
    return True


@dataclass(frozen=True)
class ArtifactRef:
    path: str
    digest: str
    source_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.path.strip() or self.path.startswith("/") or ".." in self.path.split("/"):
            raise ValueError("artifact path must be bounded and relative")
        if not _valid_digest(self.digest):
            raise ValueError("artifact digest must be a 64-character sha256 hex digest")
        if self.source_ref is not None and not self.source_ref.strip():
            raise ValueError("source_ref must be non-empty when supplied")


@dataclass(frozen=True)
class LineageEvent:
    event_id: str
    run_id: str
    state: EventState
    sequence_index: int
    event_time: str
    job_namespace: str
    job_name: str
    source_ref: str | None
    approval_ref: str | None
    materials: tuple[ArtifactRef, ...] = ()
    products: tuple[ArtifactRef, ...] = ()
    environment: Mapping[str, Any] = field(default_factory=dict)
    parent_run_id: str | None = None
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.run_id.strip() or not self.event_time.strip():
            raise ValueError("event_id, run_id, and event_time are required")
        if self.sequence_index < 1:
            raise ValueError("sequence_index must be positive")
        if not self.job_namespace.strip() or not self.job_name.strip():
            raise ValueError("job namespace and name are required")
        if self.canonical_effect != "NONE" or self.governance_effect != "NONE" or self.deployment:
            raise ValueError("lineage audit cannot request canonical, governance, or deployment effects")
        if self.state is EventState.START and self.products:
            raise ValueError("START cannot claim products")
        if self.state is EventState.FAIL and self.products:
            raise ValueError("FAIL cannot promote products")


@dataclass(frozen=True)
class LineageAudit:
    status: AuditStatus
    reason: str
    checked_events: int
    output_verified: bool = False
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    observed_result: str = "NOT_EVALUATED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "checked_events": self.checked_events,
            "output_verified": self.output_verified,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "scientific_conclusion": self.scientific_conclusion,
            "observed_result": self.observed_result,
        }


def _decision(status: AuditStatus, reason: str, count: int, verified: bool = False) -> LineageAudit:
    return LineageAudit(status, reason, count, verified)


def _artifact_paths_unique(artifacts: Sequence[ArtifactRef]) -> bool:
    return len({artifact.path for artifact in artifacts}) == len(artifacts)


def audit_transformation_lineage(
    events: Sequence[LineageEvent],
    *,
    expected_run_id: str,
    payloads: Mapping[str, bytes] | None = None,
) -> LineageAudit:
    count = len(events)
    if not events:
        return _decision(AuditStatus.HOLD, "LINEAGE_EMPTY", 0)
    if not expected_run_id.strip():
        return _decision(AuditStatus.INVALID, "EXPECTED_RUN_ID_MISSING", count)
    if any(event.run_id != expected_run_id for event in events):
        return _decision(AuditStatus.INVALID, "RUN_ID_SCOPE_MISMATCH", count)
    if len({event.event_id for event in events}) != count:
        return _decision(AuditStatus.INVALID, "DUPLICATE_EVENT_ID", count)
    indexes = [event.sequence_index for event in events]
    if indexes != list(range(1, count + 1)):
        return _decision(AuditStatus.INVALID, "SEQUENCE_INDEX_NOT_CONTIGUOUS", count)
    if any(not environment_is_redacted(event.environment) for event in events):
        return _decision(AuditStatus.INVALID, "SECRETS_UNREDACTED", count)
    starts = [event for event in events if event.state is EventState.START]
    terminals = [event for event in events if event.state in {EventState.COMPLETE, EventState.FAIL}]
    if len(starts) != 1 or len(terminals) != 1:
        return _decision(AuditStatus.INVALID, "RUN_STATE_CARDINALITY_INVALID", count)
    if events[0].state is not EventState.START or events[-1].state not in {EventState.COMPLETE, EventState.FAIL}:
        return _decision(AuditStatus.INVALID, "RUN_STATE_ORDER_INVALID", count)
    start, terminal = events[0], events[-1]
    if start.job_namespace != terminal.job_namespace or start.job_name != terminal.job_name:
        return _decision(AuditStatus.INVALID, "JOB_IDENTITY_DRIFT", count)
    if start.source_ref != terminal.source_ref or start.approval_ref != terminal.approval_ref:
        return _decision(AuditStatus.HOLD, "PROVENANCE_REFERENCE_DRIFT", count)
    if start.approval_ref is None or terminal.approval_ref is None:
        return _decision(AuditStatus.HOLD, "APPROVAL_REFERENCE_MISSING", count)
    if any(not _artifact_paths_unique(event.materials) or not _artifact_paths_unique(event.products) for event in events):
        return _decision(AuditStatus.INVALID, "DUPLICATE_ARTIFACT_PATH", count)
    if any(artifact.source_ref is None for event in events for artifact in (*event.materials, *event.products)):
        return _decision(AuditStatus.HOLD, "ARTIFACT_PROVENANCE_INCOMPLETE", count)
    if any(event.parent_run_id == event.run_id for event in events):
        return _decision(AuditStatus.INVALID, "SELF_PARENT_LINEAGE", count)
    if terminal.state is EventState.FAIL:
        return _decision(AuditStatus.VALID, "FAILED_RUN_RECORDED", count)
    if not terminal.products:
        return _decision(AuditStatus.HOLD, "COMPLETE_PRODUCTS_MISSING", count)
    if payloads is None:
        return _decision(AuditStatus.HOLD, "OUTPUT_BYTES_NOT_SUPPLIED", count)
    expected_paths = {artifact.path for artifact in terminal.products}
    if set(payloads) != expected_paths:
        return _decision(AuditStatus.INVALID, "OUTPUT_PATH_SET_MISMATCH", count)
    if not all(digest_bytes(payloads[artifact.path]) == artifact.digest.casefold() for artifact in terminal.products):
        return _decision(AuditStatus.HOLD, "OUTPUT_DIGEST_MISMATCH", count)
    return _decision(AuditStatus.VALID, "LINEAGE_COMPLETE_AND_OUTPUTS_VERIFIED", count, True)
