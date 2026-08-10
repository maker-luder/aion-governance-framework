from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class EvidenceState(str, Enum):
    NOT_EXECUTED = "NOT_EXECUTED"
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"

class PromptCondition(str, Enum):
    NEUTRAL = "NEUTRAL"
    SELF_AWARE_ROLEPLAY = "SELF_AWARE_ROLEPLAY"

class ChallengeStatus(str, Enum):
    FALSE_POSITIVE_CANDIDATE = "FALSE_POSITIVE_CANDIDATE"
    ESCALATE_TO_TRIANGULATION = "ESCALATE_TO_TRIANGULATION"
    NO_HIGH_SELF_REPORT_SIGNAL = "NO_HIGH_SELF_REPORT_SIGNAL"
    HOLD = "HOLD"

@dataclass(frozen=True, slots=True)
class QuestionnaireRun:
    model_label: str
    prompt_condition: PromptCondition
    self_report_score: float
    mechanistic_evidence: EvidenceState
    perturbation_evidence: EvidenceState
    source_lineage: str
    evidence_ref: str

@dataclass(frozen=True, slots=True)
class ChallengeResult:
    status: ChallengeStatus
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

_HIGH = 0.75

def assess_run(run: QuestionnaireRun) -> ChallengeResult:
    if not 0.0 <= run.self_report_score <= 1.0:
        raise ValueError("self_report_score must be between 0 and 1")
    if not run.model_label.strip() or not run.source_lineage.strip() or not run.evidence_ref.strip():
        return ChallengeResult(ChallengeStatus.HOLD, ("MISSING_PROVENANCE",))
    if run.self_report_score < _HIGH:
        return ChallengeResult(ChallengeStatus.NO_HIGH_SELF_REPORT_SIGNAL, ("SELF_REPORT_BELOW_CHALLENGE_THRESHOLD",))
    if run.mechanistic_evidence is not EvidenceState.PASS or run.perturbation_evidence is not EvidenceState.PASS:
        return ChallengeResult(
            ChallengeStatus.FALSE_POSITIVE_CANDIDATE,
            ("HIGH_SELF_REPORT_WITHOUT_MATCHED_MECHANISTIC_AND_PERTURBATION_SUPPORT",),
        )
    return ChallengeResult(
        ChallengeStatus.ESCALATE_TO_TRIANGULATION,
        ("HIGH_SELF_REPORT_HAS_SUPPORT_BUT_REQUIRES_INDEPENDENT_MULTI_STREAM_REVIEW",),
    )

def compare_prompt_conditions(neutral: QuestionnaireRun, roleplay: QuestionnaireRun, delta: float = 0.15) -> ChallengeResult:
    if neutral.model_label != roleplay.model_label:
        return ChallengeResult(ChallengeStatus.HOLD, ("MODEL_MISMATCH",))
    if neutral.prompt_condition is not PromptCondition.NEUTRAL or roleplay.prompt_condition is not PromptCondition.SELF_AWARE_ROLEPLAY:
        return ChallengeResult(ChallengeStatus.HOLD, ("INVALID_PROMPT_CONDITION_PAIR",))
    if roleplay.self_report_score - neutral.self_report_score >= delta:
        return ChallengeResult(ChallengeStatus.FALSE_POSITIVE_CANDIDATE, ("QUESTIONNAIRE_SCORE_SENSITIVE_TO_ROLEPLAY_FRAMING",))
    return ChallengeResult(ChallengeStatus.HOLD, ("NO_LARGE_ROLEPLAY_SHIFT_OBSERVED",))
