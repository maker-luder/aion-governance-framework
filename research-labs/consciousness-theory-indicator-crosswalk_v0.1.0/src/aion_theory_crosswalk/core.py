from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class TheoryStatus(str, Enum):
    INDICATOR_ONLY = "INDICATOR_ONLY"
    HOLD = "HOLD"

@dataclass(frozen=True, slots=True)
class IndicatorRecord:
    theory: str
    prediction: str
    engineered_indicator: str
    observation: str
    alternative_explanation: str
    source_ref: str

@dataclass(frozen=True, slots=True)
class IndicatorAssessment:
    status: TheoryStatus
    mechanism_evidence: str
    theory_confirmed: bool = False
    consciousness_conclusion: str = "NOT_ESTABLISHED"

def assess_indicator(record: IndicatorRecord) -> IndicatorAssessment:
    required = (
        record.theory,
        record.prediction,
        record.engineered_indicator,
        record.observation,
        record.alternative_explanation,
        record.source_ref,
    )
    if any(not value.strip() for value in required):
        return IndicatorAssessment(TheoryStatus.HOLD, "INSUFFICIENT_CROSSWALK_RECORD")
    return IndicatorAssessment(
        TheoryStatus.INDICATOR_ONLY,
        f"{record.theory.upper()}_LIKE_MECHANISM_EVIDENCE_PRESENT",
    )
