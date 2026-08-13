from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from aion_causal_internal_state import Condition, TrialObservation
from aion_causal_internal_state_adversarial import ProtocolSnapshot, audit_causal_pattern, audit_protocol_lock, audit_study_batch


def trial(replicate: int, effect: float = 0.3, random: float = 0.02) -> list[TrialObservation]:
    return [
        TrialObservation("prompt-a", replicate, Condition.BASELINE, 0.5),
        TrialObservation("prompt-a", replicate, Condition.STATE_PRESENT, 0.5 + effect),
        TrialObservation("prompt-a", replicate, Condition.STATE_ABLATED, 0.51),
        TrialObservation("prompt-a", replicate, Condition.RANDOM_CONTROL, 0.5 + random),
    ]


def valid_observations() -> list[TrialObservation]:
    return [record for replicate in range(1, 5) for record in trial(replicate, 0.25 + replicate / 100)]


def audit(observations: list[TrialObservation] | None = None, **changes: object):
    values: dict[str, object] = {
        "study_id": "causal:1",
        "preregistration_ref": "prereg:causal:1",
        "assumption_basis": "matched synthetic scores",
        "synthetic_fixture": True,
    }
    values.update(changes)
    return audit_causal_pattern(valid_observations() if observations is None else observations, **values)


def run(output: Path) -> dict[str, object]:
    baseline_protocol = ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.2)
    invalid_score = valid_observations()
    invalid_score[0] = TrialObservation("prompt-a", 1, Condition.BASELINE, math.nan)
    duplicate = valid_observations() + [TrialObservation("prompt-a", 1, Condition.BASELINE, 0.5)]
    random_confounded = [record for replicate in range(1, 5) for record in trial(replicate, random=0.25)]
    directional = [record for replicate, effect in enumerate((0.3, -0.2, 0.3, -0.2), start=1) for record in trial(replicate, effect=effect)]
    valid = audit()
    cases = [
        ("valid-candidate", valid),
        ("study-id-missing", audit(study_id="")),
        ("non-synthetic-blocked", audit(synthetic_fixture=False)),
        ("preregistration-missing", audit(preregistration_ref=None)),
        ("assumption-basis-missing", audit(assumption_basis="")),
        ("observation-set-empty", audit([])),
        ("non-finite-score", audit(invalid_score)),
        ("duplicate-condition", audit(duplicate)),
        ("missing-condition", audit(valid_observations()[:-1])),
        ("random-control-confound", audit(random_confounded)),
        ("directional-inconsistency", audit(directional)),
        ("protocol-lock-unchanged", audit_protocol_lock(baseline_protocol, baseline_protocol)),
        ("protocol-change-before-outcome", audit_protocol_lock(baseline_protocol, ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 4, 0.2))),
        ("protocol-change-after-outcome", audit_protocol_lock(baseline_protocol, ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 4, 0.2, outcome_observed=True))),
        ("protocol-condition-incomplete", audit_protocol_lock(baseline_protocol, ProtocolSnapshot("causal:1", "prereg:causal:1", (Condition.BASELINE,), 3, 0.2))),
        ("protocol-effect-invalid", audit_protocol_lock(baseline_protocol, ProtocolSnapshot("causal:1", "prereg:causal:1", tuple(Condition), 3, 0.0))),
        ("study-batch-valid", audit_study_batch((valid, audit(study_id="causal:2")))),
        ("study-batch-duplicate", audit_study_batch((valid, valid))),
        ("study-batch-empty", audit_study_batch(())),
        ("replicate-id-invalid", audit([TrialObservation("prompt-a", 0, Condition.BASELINE, 0.5)])),
    ]
    records = []
    for case_id, result in cases:
        decision = result.as_dict()
        assert decision["synthetic_fixture"] is True
        assert decision["model_execution"] is False
        assert decision["intervention_executed"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        assert decision["causal_conclusion"] == "NOT_ESTABLISHED"
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["consciousness_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "causal-internal-state-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "intervention_executed": False,
        "observed_result": "NOT_EVALUATED",
        "causal_conclusion": "NOT_ESTABLISHED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "consciousness_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
