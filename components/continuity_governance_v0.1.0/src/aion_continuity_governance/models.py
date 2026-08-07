from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ContinuityLayer(str, Enum):
    ACCOUNT = "ACCOUNT"
    DATA = "DATA"
    FUNCTIONAL = "FUNCTIONAL"
    INTERPRETIVE = "INTERPRETIVE"
    RELATIONAL = "RELATIONAL"


class ContinuityDimension(str, Enum):
    FACTUAL = "FACTUAL"
    PROJECT = "PROJECT"
    ROLE = "ROLE"
    INTERPRETIVE = "INTERPRETIVE"
    RELATIONAL_STYLE = "RELATIONAL_STYLE"
    CORRECTION_RECOVERY = "CORRECTION_RECOVERY"


class DriftDecision(str, Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    HOLD = "HOLD"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class DriftResult:
    decision: DriftDecision
    missing_required_terms: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class DimensionObservation:
    dimension: ContinuityDimension
    decision: DriftDecision
    evidence_refs: tuple[str, ...] = ()
    note: str = ""


@dataclass(frozen=True, slots=True)
class ContinuityMatrix:
    observations: tuple[DimensionObservation, ...]
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_continuity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
