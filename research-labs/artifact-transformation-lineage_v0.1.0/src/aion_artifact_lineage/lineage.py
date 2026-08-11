from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping


def hash_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


@dataclass(frozen=True)
class ArtifactRef:
    path: str
    digest: str
    algorithm: str = "sha256"
    source_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.path.strip():
            raise ValueError("artifact path must be non-empty")
        if self.algorithm != "sha256":
            raise ValueError("v0.1.0 supports sha256 only")
        if len(self.digest) != 64 or any(c not in "0123456789abcdef" for c in self.digest.lower()):
            raise ValueError("digest must be a 64-character sha256 hex digest")


def verify_artifact_bytes(ref: ArtifactRef, data: bytes) -> bool:
    return hash_bytes(data) == ref.digest.lower()


@dataclass(frozen=True)
class TransformationJob:
    namespace: str
    name: str
    source_code_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.namespace.strip() or not self.name.strip():
            raise ValueError("job namespace/name must be non-empty")


@dataclass(frozen=True)
class TransformationPlan:
    job: TransformationJob
    declared_inputs: tuple[ArtifactRef, ...]
    declared_outputs: tuple[str, ...]
    method_ref: str
    approval_ref: str

    def __post_init__(self) -> None:
        if not self.method_ref.strip() or not self.approval_ref.strip():
            raise ValueError("method_ref and approval_ref are required")
        if not self.declared_inputs:
            raise ValueError("at least one declared input is required")
        if len(set(self.declared_outputs)) != len(self.declared_outputs):
            raise ValueError("declared output paths must be unique")


class RunState(str, Enum):
    START = "START"
    COMPLETE = "COMPLETE"
    FAIL = "FAIL"


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


def sanitize_environment(environment: Mapping[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in environment.items():
        folded = key.casefold()
        if any(marker in folded for marker in _SECRET_MARKERS):
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    return sanitized


@dataclass(frozen=True)
class TransformationRunEvent:
    run_id: str
    job: TransformationJob
    state: RunState
    event_time: str
    materials: tuple[ArtifactRef, ...] = ()
    products: tuple[ArtifactRef, ...] = ()
    command: tuple[str, ...] = ()
    byproducts: Mapping[str, Any] = field(default_factory=dict)
    environment: Mapping[str, Any] = field(default_factory=dict)
    source_ref: str = ""
    approval_ref: str = ""
    parent_run_id: str | None = None
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.run_id.strip() or not self.event_time.strip():
            raise ValueError("run_id and event_time are required")
        if not self.source_ref.strip() or not self.approval_ref.strip():
            raise ValueError("source_ref and approval_ref are required")
        if self.canonical_effect != "NONE":
            raise ValueError("transformation lineage cannot write canonical state")
        object.__setattr__(self, "environment", sanitize_environment(self.environment))
        if self.state is RunState.START and self.products:
            raise ValueError("START event cannot claim produced artifacts")
        if self.state is RunState.FAIL and self.products:
            raise ValueError("FAIL event cannot promote produced artifacts")


class TransformationLedger:
    def __init__(self) -> None:
        self._events: list[TransformationRunEvent] = []
        self._states: dict[str, RunState] = {}
        self._jobs: dict[str, TransformationJob] = {}

    @property
    def events(self) -> tuple[TransformationRunEvent, ...]:
        return tuple(self._events)

    def append(self, event: TransformationRunEvent) -> None:
        prior = self._states.get(event.run_id)
        if event.state is RunState.START:
            if prior is not None:
                raise ValueError("run already started")
            self._jobs[event.run_id] = event.job
        else:
            if prior is not RunState.START:
                raise ValueError("terminal event requires prior START")
            if self._jobs[event.run_id] != event.job:
                raise ValueError("job changed within run")
        self._events.append(event)
        self._states[event.run_id] = event.state

    def verify_products(self, run_id: str, payloads: Mapping[str, bytes]) -> bool:
        terminal = next(
            (event for event in reversed(self._events) if event.run_id == run_id and event.state is RunState.COMPLETE),
            None,
        )
        if terminal is None:
            raise ValueError("no COMPLETE event for run")
        if set(payloads) != {ref.path for ref in terminal.products}:
            return False
        return all(verify_artifact_bytes(ref, payloads[ref.path]) for ref in terminal.products)

    def lineage_for(self, run_id: str) -> tuple[TransformationRunEvent, ...]:
        return tuple(event for event in self._events if event.run_id == run_id)
