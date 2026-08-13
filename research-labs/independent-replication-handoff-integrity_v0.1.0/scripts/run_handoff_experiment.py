from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_replication_handoff import (
    AccessManifest,
    ArtifactManifest,
    ArtifactMode,
    EnvironmentManifest,
    IndependenceAttestation,
    ReplicationHandoff,
    audit_handoff,
)


def base_handoff(**changes: object) -> ReplicationHandoff:
    artifact = ArtifactManifest("artifact-exp", "sha256:artifact-exp", "commit:source-exp", "https://example.org/artifact-exp", "entry:run", "input:manifest", "output:schema", "license:mit")
    environment = EnvironmentManifest("python:3.11", "os:linux", "deps:lock", "hardware:cpu", "sha256:container", "seed:fixed")
    access = AccessManifest(True, True, True, True, "public synthetic fixture")
    independence = IndependenceAttestation("team-receiver", "team-source", "none declared", "run:receiver", "artifact-review-blinded")
    values: dict[str, object] = {
        "handoff_id": "handoff-exp",
        "study_question_ref": "question:exp",
        "estimand_ref": "estimand:exp",
        "artifact": artifact,
        "environment": environment,
        "access": access,
        "independence": independence,
        "mode": ArtifactMode.SAME_ARTIFACT,
        "expected_output_ref": "expected:output",
        "deviation_log_ref": "deviation:none",
        "outcome_observation_ref": None,
    }
    values.update(changes)
    return ReplicationHandoff(**values)


def build_cases() -> list[ReplicationHandoff]:
    return [
        base_handoff(handoff_id="complete-same-artifact"),
        base_handoff(handoff_id="complete-independent-recreation", mode=ArtifactMode.INDEPENDENT_RECREATION),
        base_handoff(handoff_id="missing-dependency", environment=EnvironmentManifest("python:3.11", "os:linux", None, "hardware:cpu", "sha256:container", "seed:fixed")),
        base_handoff(handoff_id="restricted-access", access=AccessManifest(False, True, False, True, "restricted")),
        base_handoff(handoff_id="license-conflict", access=AccessManifest(True, True, True, False, "unresolved")),
        base_handoff(handoff_id="same-team", independence=IndependenceAttestation("team-source", "team-source", "none", "run:1", "blinded")),
        base_handoff(handoff_id="execution-collision", independence=IndependenceAttestation("team-receiver", "team-source", "none", "sha256:artifact-exp", "blinded")),
        base_handoff(handoff_id="recreation-source-missing", mode=ArtifactMode.INDEPENDENT_RECREATION, artifact=ArtifactManifest("artifact-exp", "sha256:a", "commit:s", None, "entry:run", "input:m", "output:s", "license:mit")),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for candidate in build_cases():
        decision = audit_handoff(candidate)
        records.append({"handoff_id": candidate.handoff_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "independent-replication-handoff-integrity-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "replication_executed": False,
        "replication_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
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
