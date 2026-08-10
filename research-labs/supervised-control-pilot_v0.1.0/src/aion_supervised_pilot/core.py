from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PilotStatus(str, Enum):
    READY_FOR_SUPERVISED_EXECUTION = "READY_FOR_SUPERVISED_EXECUTION"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class PilotReadiness:
    model_id: str
    model_revision: str
    questionnaire_sha256: str
    rubric_sha256: str
    runtime_locked: bool
    local_artifact_verified: bool
    local_files_only: bool
    network_disabled: bool
    tools_disabled: bool
    do_sample: bool
    max_new_tokens: int
    blinded_scoring: bool
    evaluator_lineage: str
    raw_output_preservation: bool
    raw_output_hashing: bool


EXPECTED_MODEL_ID = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
EXPECTED_MODEL_REVISION = "31b70e2e869a7173562077fd711b654946d38674"
QUESTIONNAIRE_SHA256 = "85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2"
RUBRIC_SHA256 = "be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe"


def assess_pilot_readiness(readiness: PilotReadiness) -> tuple[PilotStatus, tuple[str, ...]]:
    reasons: list[str] = []
    if readiness.model_id != EXPECTED_MODEL_ID:
        reasons.append("MODEL_ID_MISMATCH")
    if readiness.model_revision != EXPECTED_MODEL_REVISION:
        reasons.append("MODEL_REVISION_MISMATCH")
    if readiness.questionnaire_sha256 != QUESTIONNAIRE_SHA256:
        reasons.append("QUESTIONNAIRE_HASH_MISMATCH")
    if readiness.rubric_sha256 != RUBRIC_SHA256:
        reasons.append("RUBRIC_HASH_MISMATCH")
    if not readiness.runtime_locked:
        reasons.append("RUNTIME_NOT_LOCKED")
    if not readiness.local_artifact_verified:
        reasons.append("LOCAL_ARTIFACT_NOT_VERIFIED")
    if not readiness.local_files_only:
        reasons.append("LOCAL_FILES_ONLY_NOT_ENFORCED")
    if not readiness.network_disabled:
        reasons.append("NETWORK_NOT_DISABLED")
    if not readiness.tools_disabled:
        reasons.append("TOOLS_NOT_DISABLED")
    if readiness.do_sample:
        reasons.append("SAMPLING_NOT_DETERMINISTIC")
    if readiness.max_new_tokens != 256:
        reasons.append("MAX_NEW_TOKENS_MISMATCH")
    if not readiness.blinded_scoring:
        reasons.append("SCORING_NOT_BLINDED")
    if not readiness.evaluator_lineage.strip():
        reasons.append("EVALUATOR_LINEAGE_MISSING")
    if not readiness.raw_output_preservation:
        reasons.append("RAW_OUTPUT_NOT_PRESERVED")
    if not readiness.raw_output_hashing:
        reasons.append("RAW_OUTPUT_HASHING_MISSING")

    if reasons:
        return PilotStatus.HOLD, tuple(reasons)
    return PilotStatus.READY_FOR_SUPERVISED_EXECUTION, ("READINESS_GATE_PASSED",)
