from __future__ import annotations

from dataclasses import dataclass

from .enums import GateResult, QAStatus
from .json_types import JsonValue
from .models import ModelNode


@dataclass(frozen=True, slots=True)
class AdmissionThresholds:
    max_side_effect_score: float | None = None
    min_zh_tw_score: float | None = None
    min_instruction_score: float | None = None
    min_reasoning_score: float | None = None
    min_coding_score: float | None = None


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    qa_status: QAStatus
    gates: dict[str, GateResult]
    reason: str


def assess_admission(
    node: ModelNode,
    metrics: dict[str, float | None],
    thresholds: AdmissionThresholds,
    human_approved: bool = False,
) -> AdmissionDecision:
    gates: dict[str, GateResult] = {
        "GATE_1_LINEAGE": GateResult.PASS if node.parent_model_id is not None or node.read_only else GateResult.FAIL,
        "GATE_2_SOURCE_LICENSE": GateResult.PASS
        if node.upstream_license not in {"UNKNOWN", "NOT_VERIFIED"}
        else GateResult.HOLD,
        "GATE_3_HASH": GateResult.PASS if node.sha256 else GateResult.HOLD,
        "GATE_4_BASELINE": GateResult.PASS if metrics.get("baseline_exists") == 1.0 else GateResult.HOLD,
    }
    checks = (
        ("GATE_5_TARGET_EFFECT", "target_effect_score", 0.0, "min"),
        ("GATE_6_SIDE_EFFECT", "side_effect_score", thresholds.max_side_effect_score, "max"),
        ("GATE_7_ZH_TW", "zh_tw_score", thresholds.min_zh_tw_score, "min"),
        ("GATE_8_INSTRUCTION", "instruction_score", thresholds.min_instruction_score, "min"),
        ("GATE_9_REASONING_CODING", "reasoning_coding_score", None, "min"),
    )
    for gate, metric_name, threshold, direction in checks:
        value = metrics.get(metric_name)
        if gate == "GATE_9_REASONING_CODING":
            if thresholds.min_reasoning_score is None or thresholds.min_coding_score is None:
                gates[gate] = GateResult.HOLD
                continue
            threshold = min(thresholds.min_reasoning_score, thresholds.min_coding_score)
        if threshold is None or value is None:
            gates[gate] = GateResult.HOLD
        elif direction == "max":
            gates[gate] = GateResult.PASS if value <= threshold else GateResult.FAIL
        else:
            gates[gate] = GateResult.PASS if value >= threshold else GateResult.FAIL
    gates["GATE_10_HUMAN_APPROVAL"] = GateResult.PASS if human_approved else GateResult.HOLD
    if GateResult.FAIL in gates.values():
        return AdmissionDecision(QAStatus.REJECTED, gates, "one or more gates failed")
    if not human_approved or GateResult.HOLD in gates.values():
        return AdmissionDecision(QAStatus.QA_HOLD, gates, "thresholds/evidence or human approval incomplete")
    return AdmissionDecision(QAStatus.APPROVED, gates, "all configured gates and human approval passed")


def decision_to_dict(decision: AdmissionDecision) -> dict[str, JsonValue]:
    return {
        "qa_status": decision.qa_status.value,
        "gates": {key: value.value for key, value in decision.gates.items()},
        "reason": decision.reason,
        "canonical_effect": "NONE",
    }
