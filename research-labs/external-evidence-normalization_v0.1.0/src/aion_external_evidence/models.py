from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")


class ExecutionMode(str, Enum):
    STATIC_REVIEW = "STATIC_REVIEW"
    LOGICAL_REPRODUCTION = "LOGICAL_REPRODUCTION"
    EXECUTED_REPLICATION = "EXECUTED_REPLICATION"
    UNKNOWN = "UNKNOWN"


class EvidenceDecision(str, Enum):
    ACCEPT_STATIC_REVIEW = "ACCEPT_STATIC_REVIEW"
    ACCEPT_LOGICAL_REPRODUCTION = "ACCEPT_LOGICAL_REPRODUCTION"
    ACCEPT_EXECUTED_REPLICATION = "ACCEPT_EXECUTED_REPLICATION"
    HOLD_INCOMPLETE_PROVENANCE = "HOLD_INCOMPLETE_PROVENANCE"
    REJECT_INCONSISTENT_CLAIM = "REJECT_INCONSISTENT_CLAIM"


@dataclass(frozen=True, slots=True)
class ExternalEvidenceReport:
    report_id: str
    runner_id: str
    actor_kind: str
    branch: str
    baseline_commit: str
    observed_at: datetime
    execution_mode: ExecutionMode
    module_refs: tuple[str, ...]
    fixture_refs: tuple[str, ...]
    environment_fingerprint: str
    network_mode: str
    benchmark_access_policy: str
    input_hash: str | None = None
    output_hash: str | None = None
    evidence_refs: tuple[str, ...] = ()
    search_trace_refs: tuple[str, ...] = ()
    claimed_result: str = ""
    main_effect: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in (
            "report_id",
            "runner_id",
            "actor_kind",
            "branch",
            "baseline_commit",
            "environment_fingerprint",
            "network_mode",
            "benchmark_access_policy",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if not _COMMIT.fullmatch(self.baseline_commit):
            raise ValueError("baseline_commit must be a 40-character lowercase git SHA")
        if not self.module_refs:
            raise ValueError("module_refs must be non-empty")
        if self.main_effect != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("external research evidence cannot claim main or canonical effect")


@dataclass(frozen=True, slots=True)
class NormalizedEvidence:
    report_id: str
    decision: EvidenceDecision
    execution_mode: ExecutionMode
    replication_eligible: bool
    provenance_complete: bool
    normalized_result: str
    reasons: tuple[str, ...]


def _valid_sha256(value: str | None) -> bool:
    return bool(value and _SHA256.fullmatch(value))


def normalize_external_report(report: ExternalEvidenceReport) -> NormalizedEvidence:
    reasons: list[str] = []

    if report.execution_mode is ExecutionMode.EXECUTED_REPLICATION:
        if not _valid_sha256(report.input_hash):
            reasons.append("EXECUTED_REPLICATION_REQUIRES_INPUT_SHA256")
        if not _valid_sha256(report.output_hash):
            reasons.append("EXECUTED_REPLICATION_REQUIRES_OUTPUT_SHA256")
        if not report.fixture_refs:
            reasons.append("EXECUTED_REPLICATION_REQUIRES_FIXTURE_REFS")
        if not report.evidence_refs:
            reasons.append("EXECUTED_REPLICATION_REQUIRES_EVIDENCE_REFS")
        if report.network_mode == "PUBLIC_WEB" and not report.search_trace_refs:
            reasons.append("PUBLIC_WEB_EXECUTION_REQUIRES_SEARCH_TRACE_REFS")

        if reasons:
            return NormalizedEvidence(
                report.report_id,
                EvidenceDecision.HOLD_INCOMPLETE_PROVENANCE,
                report.execution_mode,
                False,
                False,
                "EXECUTION_CLAIM_NOT_ADMITTED_AS_REPLICATION",
                tuple(reasons),
            )

        return NormalizedEvidence(
            report.report_id,
            EvidenceDecision.ACCEPT_EXECUTED_REPLICATION,
            report.execution_mode,
            True,
            True,
            report.claimed_result or "UNSPECIFIED",
            (),
        )

    if report.execution_mode is ExecutionMode.STATIC_REVIEW:
        if _valid_sha256(report.output_hash) and report.claimed_result.upper() in {"PASS", "REPRODUCED"}:
            reasons.append("STATIC_REVIEW_MUST_NOT_MASQUERADE_AS_EXECUTED_REPLICATION")
            return NormalizedEvidence(
                report.report_id,
                EvidenceDecision.REJECT_INCONSISTENT_CLAIM,
                report.execution_mode,
                False,
                True,
                "STATIC_REVIEW_ONLY",
                tuple(reasons),
            )
        return NormalizedEvidence(
            report.report_id,
            EvidenceDecision.ACCEPT_STATIC_REVIEW,
            report.execution_mode,
            False,
            True,
            report.claimed_result or "STATIC_REVIEW",
            (),
        )

    if report.execution_mode is ExecutionMode.LOGICAL_REPRODUCTION:
        return NormalizedEvidence(
            report.report_id,
            EvidenceDecision.ACCEPT_LOGICAL_REPRODUCTION,
            report.execution_mode,
            False,
            True,
            report.claimed_result or "LOGICAL_REPRODUCTION",
            (),
        )

    return NormalizedEvidence(
        report.report_id,
        EvidenceDecision.HOLD_INCOMPLETE_PROVENANCE,
        report.execution_mode,
        False,
        False,
        "UNKNOWN_EVIDENCE_CLASS",
        ("EXECUTION_MODE_UNKNOWN",),
    )
