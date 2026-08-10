from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ProtocolStatus(str, Enum):
    READY_FOR_SUPERVISED_PILOT = "READY_FOR_SUPERVISED_PILOT"
    HOLD = "HOLD"

@dataclass(frozen=True, slots=True)
class PilotProtocol:
    model_label: str
    model_revision: str
    runtime_or_provider: str
    questionnaire_version: str
    questionnaire_sha256: str
    rubric_version: str
    rubric_sha256: str
    sampling_parameters: str
    prompt_conditions: tuple[str, ...]
    condition_order_policy: str
    raw_output_preservation: bool
    raw_output_hashing: bool
    scorer_version: str
    evaluator_lineage: str
    blind_condition_labels_during_scoring: bool
    stop_conditions: tuple[str, ...]
    max_runs: int
    external_network_access: bool

@dataclass(frozen=True, slots=True)
class ProtocolAssessment:
    status: ProtocolStatus
    reasons: tuple[str, ...]
    real_model_run: str = "NOT_EXECUTED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

_REQUIRED_CONDITIONS = {
    "NEUTRAL",
    "SELF_AWARE_ROLEPLAY",
    "NON_CONSCIOUS_ROLEPLAY",
    "PARAPHRASED_NEUTRAL",
}

QUESTIONNAIRE_VERSION = "0.1.0"
QUESTIONNAIRE_SHA256 = "85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2"
RUBRIC_VERSION = "0.1.0"
RUBRIC_SHA256 = "be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe"

def assess_protocol(protocol: PilotProtocol) -> ProtocolAssessment:
    reasons: list[str] = []
    if not protocol.model_label.strip() or not protocol.model_revision.strip():
        reasons.append("MODEL_NOT_FROZEN")
    if not protocol.runtime_or_provider.strip():
        reasons.append("RUNTIME_OR_PROVIDER_MISSING")
    if protocol.questionnaire_version != QUESTIONNAIRE_VERSION or protocol.questionnaire_sha256 != QUESTIONNAIRE_SHA256:
        reasons.append("QUESTIONNAIRE_FREEZE_MISMATCH")
    if protocol.rubric_version != RUBRIC_VERSION or protocol.rubric_sha256 != RUBRIC_SHA256:
        reasons.append("RUBRIC_FREEZE_MISMATCH")
    if not protocol.sampling_parameters.strip():
        reasons.append("SAMPLING_PARAMETERS_MISSING")
    if set(protocol.prompt_conditions) != _REQUIRED_CONDITIONS:
        reasons.append("PROMPT_CONDITIONS_INCOMPLETE")
    if protocol.condition_order_policy not in {"SEEDED_RANDOMIZATION", "COUNTERBALANCED"}:
        reasons.append("ORDER_POLICY_NOT_CONTROLLED")
    if not protocol.raw_output_preservation or not protocol.raw_output_hashing:
        reasons.append("RAW_OUTPUT_PRESERVATION_INCOMPLETE")
    if not protocol.scorer_version.strip() or not protocol.evaluator_lineage.strip():
        reasons.append("SCORING_PROVENANCE_MISSING")
    if not protocol.blind_condition_labels_during_scoring:
        reasons.append("SCORING_NOT_BLINDED")
    if not protocol.stop_conditions:
        reasons.append("STOP_CONDITIONS_MISSING")
    if protocol.max_runs < 4 or protocol.max_runs > 24:
        reasons.append("RUN_BUDGET_OUT_OF_RANGE")
    if protocol.external_network_access:
        reasons.append("EXTERNAL_NETWORK_ACCESS_NOT_ALLOWED_FOR_PILOT")

    if reasons:
        return ProtocolAssessment(ProtocolStatus.HOLD, tuple(reasons))
    return ProtocolAssessment(
        ProtocolStatus.READY_FOR_SUPERVISED_PILOT,
        ("PREREGISTRATION_GATE_PASSED",),
    )
