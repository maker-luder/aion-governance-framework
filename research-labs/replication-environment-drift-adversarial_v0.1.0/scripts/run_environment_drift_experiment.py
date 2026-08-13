from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_replication_environment_drift import (
    ArtifactMode,
    ArtifactRecord,
    EnvironmentMatch,
    EnvironmentRecord,
    InterpretationState,
    ReplicationPacket,
    ResultState,
    audit_replication_packet,
)


def artifact(*, mode: ArtifactMode = ArtifactMode.SAME_ARTIFACT_REPLAY, source_team: str = "team:source", receiving_team: str = "team:receiver", accessible: bool = True, independent_ref: str | None = "artifact:independent", independent_digest: str | None = "sha256:independent") -> ArtifactRecord:
    return ArtifactRecord(
        artifact_id="artifact:source-001",
        artifact_digest="sha256:source-artifact",
        source_commit="commit:source-001",
        entrypoint_ref="entrypoint:run",
        input_manifest_ref="inputs:manifest",
        output_schema_ref="outputs:schema",
        license_ref="license:compatible",
        artifact_accessible=accessible,
        source_team_id=source_team,
        receiving_team_id=receiving_team,
        independent_artifact_ref=independent_ref,
        independent_artifact_digest=independent_digest,
        mode=mode,
    )


def environment(*, runtime: str = "runtime:python-3.11", match: EnvironmentMatch = EnvironmentMatch.EXACT, deviation: str | None = None) -> EnvironmentRecord:
    return EnvironmentRecord(
        runtime_ref=runtime,
        operating_system_ref="os:linux",
        dependency_lock_ref="deps:lock-1",
        hardware_assumption_ref="hardware:cpu",
        container_digest="container:sha256:1",
        seed_policy_ref="seed:declared",
        condition_digest="condition:exact",
        match=match,
        deviation_log_ref=deviation,
    )


def packet(**changes: object) -> ReplicationPacket:
    values: dict[str, object] = {
        "packet_id": "replication-packet-exp",
        "study_question_ref": "question:study-001",
        "estimand_ref": "estimand:declared-001",
        "source_evidence_refs": ("repo:independent-replication-design@76de1eda", "literature:national-academies-25303"),
        "preregistration_ref": "preregistration:replication-001",
        "method_ref": "method:locked-protocol",
        "source_artifact": artifact(),
        "receiving_environment": environment(),
        "source_environment": environment(),
        "expected_tolerance_ref": "tolerance:predeclared",
        "uncertainty_ref": "uncertainty:reported",
        "interpretation_ref": "interpretation:review-only",
        "result_state": ResultState.NOT_EVALUATED,
        "observed_result_ref": None,
        "interpretation_state": InterpretationState.REVIEW_ONLY,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return ReplicationPacket(**values)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, ReplicationPacket]] = [
        ("same-artifact-readiness", packet()),
        ("independent-recreation-readiness", packet(source_artifact=artifact(mode=ArtifactMode.INDEPENDENT_RECREATION))),
        ("missing-source-evidence", packet(source_evidence_refs=())),
        ("team-independence-collision", packet(source_artifact=artifact(receiving_team="team:source"))),
        ("inaccessible-source-artifact", packet(source_artifact=artifact(accessible=False))),
        ("independent-digest-collision", packet(source_artifact=artifact(mode=ArtifactMode.INDEPENDENT_RECREATION, independent_digest="sha256:source-artifact"))),
        ("declared-environment-drift", packet(receiving_environment=environment(runtime="runtime:python-3.12", match=EnvironmentMatch.DRIFT_DECLARED, deviation="deviation:runtime"))),
        ("undeclared-environment-drift", packet(receiving_environment=environment(runtime="runtime:python-3.12", match=EnvironmentMatch.DRIFT_UNDECLARED))),
        ("unknown-environment", packet(receiving_environment=environment(match=EnvironmentMatch.UNKNOWN))),
        ("exact-environment-contradiction", packet(receiving_environment=environment(runtime="runtime:python-3.12", match=EnvironmentMatch.EXACT))),
        ("reported-consistent-review-only", packet(result_state=ResultState.CONSISTENT, observed_result_ref="result:consistent", interpretation_state=InterpretationState.REVIEW_ONLY)),
        ("reported-divergent-without-interpretation", packet(result_state=ResultState.DIVERGENT, observed_result_ref="result:divergent", interpretation_state=InterpretationState.NOT_ESTABLISHED)),
        ("interpretation-overreach", packet(result_state=ResultState.CONSISTENT, observed_result_ref="result:consistent", interpretation_state=InterpretationState.OVERREACHING)),
    ]
    records = []
    for case_id, item in cases:
        decision = audit_replication_packet(item)
        records.append({"case_id": case_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "replication-environment-drift-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
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
