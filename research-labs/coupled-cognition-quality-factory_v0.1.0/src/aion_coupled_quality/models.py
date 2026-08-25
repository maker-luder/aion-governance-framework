from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum


class QualityError(ValueError):
    pass


class FactoryStage(StrEnum):
    INTAKE = "INTAKE"
    IQC = "IQC"
    HYPOTHESIS = "HYPOTHESIS"
    AI_WORK = "AI_WORK"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    IPQC = "IPQC"
    COUNTEREVIDENCE = "COUNTEREVIDENCE"
    IMPLEMENT = "IMPLEMENT"
    VERIFY = "VERIFY"
    FINAL_QA = "FINAL_QA"
    RELEASED = "RELEASED"
    HOLD = "HOLD"


class EvidenceKind(StrEnum):
    EXTERNAL_PRIMARY = "EXTERNAL_PRIMARY"
    EXTERNAL_SECONDARY = "EXTERNAL_SECONDARY"
    REPOSITORY_ARTIFACT = "REPOSITORY_ARTIFACT"
    TEST_RESULT = "TEST_RESULT"
    HUMAN_OBSERVATION = "HUMAN_OBSERVATION"
    MODEL_OUTPUT = "MODEL_OUTPUT"
    COUNTEREVIDENCE = "COUNTEREVIDENCE"


class CounterDisposition(StrEnum):
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    REBUTTED_WITH_EVIDENCE = "REBUTTED_WITH_EVIDENCE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class Severity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class NCRState(StrEnum):
    OPEN = "OPEN"
    CONTAINED = "CONTAINED"
    CAPA_PLANNED = "CAPA_PLANNED"
    CAPA_APPLIED = "CAPA_APPLIED"
    EFFECTIVENESS_VERIFIED = "EFFECTIVENESS_VERIFIED"
    CLOSED = "CLOSED"


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    kind: EvidenceKind
    reference: str
    supports_claim: bool
    independent_of_current_pair: bool = False


@dataclass(slots=True)
class CounterEvidenceItem:
    item_id: str
    reference: str
    challenge: str
    disposition: CounterDisposition = CounterDisposition.OPEN
    resolution_evidence_refs: tuple[str, ...] = ()


@dataclass(slots=True)
class NCR:
    ncr_id: str
    defect: str
    severity: Severity
    root_cause_hypothesis: str = "UNESTABLISHED"
    state: NCRState = NCRState.OPEN
    capa_action: str = ""
    verification_refs: tuple[str, ...] = ()


@dataclass(slots=True)
class ResearchLot:
    lot_id: str
    claim: str
    risk: Severity = Severity.MEDIUM
    stage: FactoryStage = FactoryStage.INTAKE
    evidence: list[Evidence] = field(default_factory=list)
    counterevidence: list[CounterEvidenceItem] = field(default_factory=list)
    ncrs: list[NCR] = field(default_factory=list)
    human_approved: bool = False
    ai_supported: bool = False
    hypothesis_falsifier: str = ""
    final_qa_pass: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False
