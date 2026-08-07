from __future__ import annotations

from dataclasses import dataclass

from .enums import CanonicalEffect, QAStatus


@dataclass(frozen=True, slots=True)
class WritebackRequest:
    source_provenance_valid: bool = False
    evidence_manifest_valid: bool = False
    lineage_chain_valid: bool = False
    qa_status: QAStatus = QAStatus.QA_HOLD
    human_approval_reference: str | None = None
    unresolved_conflict: bool = True
    identity_pollution: bool = True
    canonical_effect: CanonicalEffect = CanonicalEffect.NONE


@dataclass(frozen=True, slots=True)
class WritebackDecision:
    canonical_writeback: str
    qa_status: QAStatus
    reasons: tuple[str, ...]


def evaluate_writeback(request: WritebackRequest) -> WritebackDecision:
    reasons: list[str] = []
    checks = (
        (request.source_provenance_valid, "source provenance invalid"),
        (request.evidence_manifest_valid, "evidence manifest invalid"),
        (request.lineage_chain_valid, "lineage chain invalid"),
        (request.qa_status is QAStatus.APPROVED, "QA approval missing"),
        (bool(request.human_approval_reference), "human approval missing"),
        (not request.unresolved_conflict, "unresolved conflict exists"),
        (not request.identity_pollution, "identity pollution detected"),
        (request.canonical_effect is CanonicalEffect.APPROVED, "canonical effect not explicitly approved"),
    )
    for passed, reason in checks:
        if not passed:
            reasons.append(reason)
    if reasons:
        return WritebackDecision("DENIED", QAStatus.QA_HOLD, tuple(reasons))
    return WritebackDecision("ALLOWED_FOR_HUMAN_CONTROLLED_WRITEBACK", QAStatus.APPROVED, ())


def qa_gate_status(gates: dict[str, bool | None]) -> tuple[QAStatus, tuple[str, ...]]:
    failed = tuple(name for name, value in gates.items() if value is not True)
    return (QAStatus.QA_HOLD, failed) if failed else (QAStatus.APPROVED, ())
