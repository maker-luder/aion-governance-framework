from __future__ import annotations

from .enums import Decision, EvidenceStatus, QAStatus
from .models import GateResult, SourceCard


def upstream_incident_gate(sources: tuple[SourceCard, ...], high_privilege_requested: bool) -> GateResult:
    serious_signal = any(
        source.evidence_status
        in {
            EvidenceStatus.CONFIRMED_OFFICIAL,
            EvidenceStatus.CORROBORATED_MEDIA,
            EvidenceStatus.MEDIA_REPORTED,
            EvidenceStatus.PROVIDED_SUMMARY_UNVERIFIED,
        }
        for source in sources
    )
    if serious_signal and high_privilege_requested:
        return GateResult(
            Decision.QA_HOLD,
            ("upstream incident review is active; privilege expansion is blocked",),
            QAStatus.QA_HOLD,
        )
    return GateResult(Decision.ALLOW, (), QAStatus.APPROVED)
