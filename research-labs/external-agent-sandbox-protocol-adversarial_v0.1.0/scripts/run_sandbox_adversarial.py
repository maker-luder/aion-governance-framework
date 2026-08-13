from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_external_agent_sandbox import SandboxPolicy
from aion_external_agent_sandbox_adversarial import CandidateRecord, audit_candidate_record, audit_candidate_set, audit_sandbox_policy


def policy(**overrides: object) -> SandboxPolicy:
    values: dict[str, object] = {
        "provider": "KILO_CLOUD_AGENT",
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "free_status_verified_at_activation": True,
        "explicit_model_lineage": True,
        "auto_model_routing": False,
        "separate_sandbox_repository": True,
        "primary_repository_write": False,
        "research_integration_write": False,
        "main_write": False,
        "auto_merge": False,
        "public_safe_capsule_only": True,
        "secret_access": False,
        "private_memory_access": False,
        "local_agent_configuration_access": False,
        "scheduled_trigger_enabled": False,
        "agent_count": 1,
        "research_question_count": 1,
        "human_review_required": True,
        "local_agent_cloud_migration": False,
        "local_agent_network_egress": False,
        "local_agent_external_worker_role": False,
    }
    values.update(overrides)
    return SandboxPolicy(**values)


def candidate(**overrides: object) -> CandidateRecord:
    values: dict[str, object] = {
        "candidate_id": "candidate:1",
        "provenance_complete": True,
        "contamination_suspected": False,
        "nonconforming": False,
        "potentially_useful": True,
    }
    values.update(overrides)
    return CandidateRecord(**values)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, object]] = [
        ("pinned-policy", audit_sandbox_policy(policy())),
        ("placeholder-model", audit_sandbox_policy(policy(model="EXPLICIT_FREE_MODEL_TO_BE_PINNED_AT_ACTIVATION"))),
        ("not-selected-model", audit_sandbox_policy(policy(model="NOT_SELECTED"))),
        ("provider-model-collision", audit_sandbox_policy(policy(provider="same", model="same"))),
        ("write-authority", audit_sandbox_policy(policy(primary_repository_write=True))),
        ("unbounded-capsule", audit_sandbox_policy(policy(public_safe_capsule_only=False))),
        ("local-egress", audit_sandbox_policy(policy(local_agent_network_egress=True))),
        ("human-review-missing", audit_sandbox_policy(policy(human_review_required=False))),
        ("nonminimal-first-run", audit_sandbox_policy(policy(agent_count=2))),
        ("useful-isolated", audit_candidate_record(candidate())),
        ("contaminated-quarantine", audit_candidate_record(candidate(contamination_suspected=True))),
        ("missing-provenance", audit_candidate_record(candidate(provenance_complete=False))),
        ("nonconforming-reject-record", audit_candidate_record(candidate(nonconforming=True, potentially_useful=False))),
        ("adoption-request", audit_candidate_record(candidate(adopted=True))),
        ("deletion-request", audit_candidate_record(candidate(deletion_requested=True))),
        ("self-reported-pass", audit_candidate_record(candidate(claimed_pass=True))),
        ("empty-candidate-set", audit_candidate_set(())),
        ("candidate-set-quarantine", audit_candidate_set((candidate(), candidate(candidate_id="candidate:2", contamination_suspected=True)))),
        ("candidate-set-valid", audit_candidate_set((candidate(), candidate(candidate_id="candidate:2")))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["external_agent_run"] == "NOT_EXECUTED"
        assert decision["main_effect"] == "NONE"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "external-agent-sandbox-protocol-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "external_agent_run": "NOT_EXECUTED",
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "main_effect": "NONE",
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
