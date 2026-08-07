from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ContinuityLayer(str, Enum):
    ACCOUNT = "ACCOUNT"
    DATA = "DATA"
    FUNCTIONAL = "FUNCTIONAL"
    INTERPRETIVE = "INTERPRETIVE"
    RELATIONAL = "RELATIONAL"


class DriftDecision(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class DriftResult:
    decision: DriftDecision
    missing_required_terms: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    canonical_effect: str = "NONE"
