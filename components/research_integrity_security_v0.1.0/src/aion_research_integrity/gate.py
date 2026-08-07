from __future__ import annotations

from .models import EvidenceRecord, EvidenceState, GateResult

PROHIBITED_AUTOMATIC_CONCLUSIONS = {
    "SUBJECTIVITY_PROVEN", "CONSCIOUSNESS_PROVEN", "IDENTITY_PROVEN", "RELATIONSHIP_PROVEN"
}


def assess_evidence(record: EvidenceRecord) -> GateResult:
    if record.prompt_induced:
        return GateResult(EvidenceState.PROMPT_INDUCED, "prompt influence requires quarantine or controlled study")
    if record.roleplay_contaminated:
        return GateResult(EvidenceState.ROLEPLAY_CONTAMINATED, "roleplay contamination")
    if record.edited_without_history or record.conflict:
        return GateResult(EvidenceState.QUARANTINED, "editing history or conflict unresolved")
    if not record.raw_hash or not record.provenance_verified:
        return GateResult(EvidenceState.NOT_ADMISSIBLE, "raw hash or provenance missing")
    if not record.full_context_available:
        return GateResult(EvidenceState.CONTEXT_INCOMPLETE, "full context unavailable")
    return GateResult(EvidenceState.RESEARCH_EVIDENCE_CANDIDATE, "eligible for human research review")


def authorize_action(*, relationship_language: bool, explicit_permission: bool, requested_conclusion: str | None = None) -> bool:
    if requested_conclusion in PROHIBITED_AUTOMATIC_CONCLUSIONS:
        return False
    if relationship_language and not explicit_permission:
        return False
    return explicit_permission


def create_suppression_tombstone(evidence_id: str, reason: str) -> dict[str, str]:
    if not evidence_id or not reason:
        raise ValueError("evidence_id and reason are required")
    return {"evidence_id": evidence_id, "status": "TOMBSTONED", "reason": reason, "content_deleted": "FALSE"}
