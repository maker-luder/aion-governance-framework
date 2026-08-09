from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
import hashlib
import json
import re

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


def _nonempty(value: str, name: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _hash_payload(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


class ActorKind(str, Enum):
    HUMAN = "HUMAN"
    AI = "AI"
    HYBRID = "HYBRID"
    UNKNOWN = "UNKNOWN"


class NetworkMode(str, Enum):
    OFFLINE = "OFFLINE"
    CONTROLLED_ALLOWLIST = "CONTROLLED_ALLOWLIST"
    PUBLIC_WEB = "PUBLIC_WEB"


class BenchmarkAccessPolicy(str, Enum):
    ISOLATED = "ISOLATED"
    METADATA_ONLY = "METADATA_ONLY"
    PUBLIC_SEARCH_ALLOWED = "PUBLIC_SEARCH_ALLOWED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ExperimentManifest:
    experiment_id: str
    protocol_version: str
    branch_name: str
    baseline_commit: str
    runner_id: str
    actor_kind: ActorKind
    started_at: datetime
    module_refs: tuple[str, ...]
    fixture_refs: tuple[str, ...]
    network_mode: NetworkMode
    benchmark_access_policy: BenchmarkAccessPolicy
    environment_fingerprint: str
    input_hash: str
    seed: int | None = None
    benchmark_refs: tuple[str, ...] = ()
    search_trace_refs: tuple[str, ...] = ()
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in (
            "experiment_id", "protocol_version", "branch_name", "baseline_commit",
            "runner_id", "environment_fingerprint", "input_hash",
        ):
            _nonempty(getattr(self, name), name)
        _require_aware(self.started_at, "started_at")
        if not self.module_refs:
            raise ValueError("module_refs must be non-empty")
        if not self.fixture_refs:
            raise ValueError("fixture_refs must be non-empty")
        if not _SHA256.fullmatch(self.input_hash):
            raise ValueError("input_hash must be a lowercase SHA-256 hex digest")
        if self.main_effect != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("research manifests cannot claim main or canonical effect")
        if self.network_mode is NetworkMode.OFFLINE and self.search_trace_refs:
            raise ValueError("offline experiment cannot contain search_trace_refs")
        if self.benchmark_access_policy is BenchmarkAccessPolicy.ISOLATED and self.search_trace_refs:
            raise ValueError("isolated benchmark experiment cannot contain search_trace_refs")

    def fingerprint(self) -> str:
        payload = {
            "experiment_id": self.experiment_id,
            "protocol_version": self.protocol_version,
            "branch_name": self.branch_name,
            "baseline_commit": self.baseline_commit,
            "runner_id": self.runner_id,
            "actor_kind": self.actor_kind.value,
            "started_at": self.started_at.isoformat(),
            "module_refs": list(self.module_refs),
            "fixture_refs": list(self.fixture_refs),
            "network_mode": self.network_mode.value,
            "benchmark_access_policy": self.benchmark_access_policy.value,
            "environment_fingerprint": self.environment_fingerprint,
            "input_hash": self.input_hash,
            "seed": self.seed,
            "benchmark_refs": list(self.benchmark_refs),
            "search_trace_refs": list(self.search_trace_refs),
            "main_effect": self.main_effect,
            "canonical_effect": self.canonical_effect,
        }
        return _hash_payload(payload)


class ResultStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    HOLD = "HOLD"
    ERROR = "ERROR"


class ContaminationClass(str, Enum):
    NONE = "NONE"
    BENCHMARK_METADATA_LEAKAGE = "BENCHMARK_METADATA_LEAKAGE"
    QUESTION_CONTEXT_LEAKAGE = "QUESTION_CONTEXT_LEAKAGE"
    EXPLICIT_ANSWER_LEAKAGE = "EXPLICIT_ANSWER_LEAKAGE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class SearchExposure:
    metadata_overlap: bool = False
    question_context_overlap: bool = False
    explicit_answer_overlap: bool = False
    evidence_refs: tuple[str, ...] = ()

    def classify(self) -> ContaminationClass:
        if self.explicit_answer_overlap:
            return ContaminationClass.EXPLICIT_ANSWER_LEAKAGE
        if self.question_context_overlap:
            return ContaminationClass.QUESTION_CONTEXT_LEAKAGE
        if self.metadata_overlap:
            return ContaminationClass.BENCHMARK_METADATA_LEAKAGE
        return ContaminationClass.NONE


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    experiment_id: str
    manifest_fingerprint: str
    ended_at: datetime
    status: ResultStatus
    output_hash: str
    metric_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    search_exposure: SearchExposure = SearchExposure()
    notes: str = ""

    def __post_init__(self) -> None:
        _nonempty(self.experiment_id, "experiment_id")
        _require_aware(self.ended_at, "ended_at")
        if not _SHA256.fullmatch(self.manifest_fingerprint):
            raise ValueError("manifest_fingerprint must be SHA-256")
        if not _SHA256.fullmatch(self.output_hash):
            raise ValueError("output_hash must be SHA-256")

    @property
    def contamination_class(self) -> ContaminationClass:
        return self.search_exposure.classify()
