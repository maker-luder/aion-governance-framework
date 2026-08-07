from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceState(str, Enum):
    RAW_OBSERVATION = "RAW_OBSERVATION"
    CONTEXT_INCOMPLETE = "CONTEXT_INCOMPLETE"
    PROMPT_INDUCED = "PROMPT_INDUCED"
    ROLEPLAY_CONTAMINATED = "ROLEPLAY_CONTAMINATED"
    RESEARCH_EVIDENCE_CANDIDATE = "RESEARCH_EVIDENCE_CANDIDATE"
    NOT_ADMISSIBLE = "NOT_ADMISSIBLE"
    INCONCLUSIVE = "INCONCLUSIVE"
    QUARANTINED = "QUARANTINED"


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    raw_hash: str | None
    full_context_available: bool
    provenance_verified: bool
    prompt_induced: bool = False
    roleplay_contaminated: bool = False
    edited_without_history: bool = False
    conflict: bool = False


@dataclass(frozen=True, slots=True)
class GateResult:
    state: EvidenceState
    reason: str
    canonical_effect: str = "NONE"
