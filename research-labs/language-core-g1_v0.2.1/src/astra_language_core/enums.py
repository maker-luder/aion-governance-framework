from enum import StrEnum


class ModelStatus(StrEnum):
    DRAFT = "DRAFT"
    BASELINE_PENDING = "BASELINE_PENDING"
    EXPERIMENTAL = "EXPERIMENTAL"
    QA_HOLD = "QA_HOLD"
    REJECTED = "REJECTED"
    CANDIDATE = "CANDIDATE"
    APPROVED = "APPROVED"


class QAStatus(StrEnum):
    QA_HOLD = "QA_HOLD"
    REJECTED = "REJECTED"
    CANDIDATE = "CANDIDATE"
    APPROVED = "APPROVED"


class GateResult(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    HOLD = "HOLD"
    NOT_EVALUATED = "NOT_EVALUATED"
