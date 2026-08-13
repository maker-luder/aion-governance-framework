from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_astra_matched_design import (
    ComparisonMode,
    SourceStatus,
    StudyDesign,
    StimulusPair,
    SystemSource,
    audit_study_design,
)


CURRENT_REMOTE = "76de1eda82865a37d3a0185336870739ed577153"
LOCAL_REPORTING = "713056ea77da9122d9b7659ec701dfdbfdfc90ba"


def source(system_id: str, family: str, *, state: str = CURRENT_REMOTE, status: SourceStatus = SourceStatus.CURRENT_VERIFIED, component: str | None = None, environment: str = "env:design") -> SystemSource:
    return SystemSource(
        system_id=system_id,
        family=family,
        component_ref=component or f"component:{system_id.lower()}",
        version_ref=f"version:{system_id.lower()}:v0.1.0",
        source_state_ref=state,
        source_status=status,
        environment_ref=environment,
    )


def pair(pair_id: str = "pair-1", *, order: str = "AB", prompt: str = "prompt:v1", expected: int = 2, control: int = 2) -> StimulusPair:
    return StimulusPair(
        pair_id=pair_id,
        stimulus_digest=f"sha256:stimulus-{pair_id}",
        context_digest=f"sha256:context-{pair_id}",
        prompt_version=prompt,
        expected_exposure_count=expected,
        control_exposure_count=control,
        order_assignment=order,
    )


def design(**changes: object) -> StudyDesign:
    values: dict[str, object] = {
        "study_id": "aion-astra-study-exp",
        "protocol_version": "0.1.0",
        "research_question_ref": "question:matched-divergence-mechanism",
        "estimand_ref": "estimand:declared-mechanism-outcome",
        "comparison_mode": ComparisonMode.PAIRED,
        "aion_source": source("aion-v0.1.0", "AION", component="component:aion_runtime_v0.1.0"),
        "astra_source": source("astra-v0.1.0", "ASTRA", component="component:astra_runtime_v0.1.0"),
        "source_evidence_refs": ("repo:matched-divergence-protocol-integrity@76de1eda", "repo:state-reconciliation@76de1eda"),
        "tested_source_head": CURRENT_REMOTE,
        "reporting_head": LOCAL_REPORTING,
        "preregistration_ref": "preregistration:study-exp",
        "immutable_plan_digest": "sha256:plan-exp",
        "outcome_scope": "declared mechanism-level comparison outcome",
        "comparison_rule_ref": "rule:predeclared-comparison",
        "outcome_blinding_ref": "blinding:outcome-sealed",
        "evaluator_identity_sealed": True,
        "randomization_ref": "randomization:seed-record",
        "counterbalance_ref": "counterbalance:AB-BA",
        "leakage_attestation_ref": "leakage:none-attested",
        "stopping_rule_ref": "stopping:predeclared",
        "execution_prohibition_ref": "execution:prohibited-design-only",
        "environment_ref": "env:design",
        "stimulus_pairs": (pair(order="AB"), pair("pair-2", order="BA")),
        "model_execution": False,
        "observed_result_ref": None,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return StudyDesign(**values)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, StudyDesign]] = [
        ("complete-current-source-design", design()),
        ("reporting-head-mislabeled-as-tested", design(reporting_head=CURRENT_REMOTE)),
        ("tested-source-head-drift", design(tested_source_head="40088cbc9eef5363d6eaf2feb7dc761e0f76f271")),
        ("historical-aion-source", design(aion_source=source("aion-v0.1.0", "AION", status=SourceStatus.HISTORICAL, component="component:aion_runtime_v0.1.0"))),
        ("missing-source-evidence", design(source_evidence_refs=())),
        ("system-family-mismatch", design(astra_source=source("astra-v0.1.0", "AION", component="component:astra_runtime_v0.1.0"))),
        ("environment-mismatch", design(astra_source=source("astra-v0.1.0", "ASTRA", component="component:astra_runtime_v0.1.0", environment="env:other"))),
        ("prompt-version-drift", design(stimulus_pairs=(pair(order="AB"), pair("pair-2", order="BA", prompt="prompt:v2")))),
        ("counterbalance-incomplete", design(stimulus_pairs=(pair(order="AB"), pair("pair-2", order="AB")))),
        ("model-execution-request", design(model_execution=True)),
        ("observed-result-leakage", design(observed_result_ref="result:observed")),
        ("scope-overreach", design(outcome_scope="subjectivity comparison")),
        ("boundary-effect-request", design(governance_effect="PROMOTE")),
    ]
    records = []
    for case_id, study in cases:
        decision = audit_study_design(study)
        records.append({"case_id": case_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "aion-astra-matched-divergence-study-design-only-synthetic-falsifiers",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "tested_source_head": CURRENT_REMOTE,
        "reporting_head": LOCAL_REPORTING,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
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
