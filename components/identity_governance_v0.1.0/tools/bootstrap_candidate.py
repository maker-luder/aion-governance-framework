from __future__ import annotations

import json
from pathlib import Path

from aion_astra_governance.forks import ResearchForkService
from aion_astra_governance.hashing import hash_file, hash_object
from aion_astra_governance.lineage import StateLineageLedger
from aion_astra_governance.models import (
    AnalysisChannel,
    LineageEvent,
    PerspectiveEventRecord,
    ProjectIdentityRecord,
    ResearchForkRecord,
    SystemStateRecord,
)
from aion_astra_governance.registry import CapabilityRegistry, ProjectIdentityRegistry
from aion_astra_governance.storage import write_new_json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "identity_lineage"


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def main() -> None:
    ProjectIdentityRegistry(ARTIFACTS / "identity").register(ProjectIdentityRecord("AION-ASTRA-PROJECT-001"))
    source_models = load_object(
        ROOT.parent
        / "ASTRA_LANGUAGE_CORE_RESEARCH_LAB_CANDIDATE_v0.1.0"
        / "configs"
        / "astra_language_core"
        / "models.example.yaml"
    )["models"]
    if not isinstance(source_models, list):
        raise ValueError("models must be an array")
    capabilities = CapabilityRegistry(ARTIFACTS / "capabilities")
    for item in source_models:
        if not isinstance(item, dict):
            raise ValueError("model node must be an object")
        capabilities.register(CapabilityRegistry.from_language_core_node(item))

    config = ROOT / "configs" / "identity_lineage"
    genesis = SystemStateRecord(
        state_id="AION-ASTRA-STATE-CANDIDATE-000000",
        project_id="AION-ASTRA-PROJECT-001",
        previous_state_id=None,
        sequence_number=0,
        state_type="GENESIS_CANDIDATE",
        previous_state_hash="GENESIS",
        canonical_manifest_hash="UNKNOWN",
        governance_policy_hash=hash_file(config / "governance_policy.example.yaml"),
        capability_manifest_hash=hash_file(config / "capability_manifest.example.yaml"),
        model_manifest_hash=hash_file(config / "capability_manifest.example.yaml"),
        runtime_manifest_hash=hash_file(config / "runtime_manifest.example.yaml"),
        artifact_ids=tuple(sorted(capabilities.ids())),
        notes="Candidate genesis; no canonical effect and no approval.",
    ).sealed()
    StateLineageLedger(ARTIFACTS / "lineage").append(genesis)

    fork_service = ResearchForkService(ARTIFACTS / "forks")
    for fork_id, artifact_id, fork_type in (
        ("RESEARCH-FORK-TW-LORA-002", "G1-TW-LORA", "LORA_EXPERIMENT"),
        ("RESEARCH-FORK-4B-ABLATION-003", "G1-ABLATION-LOW", "ABLATION_EXPERIMENT"),
        ("RESEARCH-FORK-RANDOM-CONTROL-001", "G1-RANDOM-CONTROL", "CONTROL_EXPERIMENT"),
        ("RESEARCH-FORK-ABLATION-TW-LORA-001", "G1-ABLATION-TW-LORA", "INTERACTION_EXPERIMENT"),
    ):
        fork_service.create(
            ResearchForkRecord(
                fork_id,
                genesis.state_id,
                genesis.state_hash,
                fork_type,
                "Register an isolated Language Core research candidate.",
                "Research hypothesis remains untested.",
                ("language_core",),
                artifact_ids=(artifact_id,),
            ),
            {"state_id": genesis.state_id, "state_hash": genesis.state_hash},
            capabilities.ids(),
        )

    perspective = PerspectiveEventRecord(
        "PERSPECTIVE-CANDIDATE-001",
        ("EXTERNAL_PROPOSAL_SOURCE_001",),
        hash_object(["EXTERNAL_PROPOSAL_SOURCE_001"]),
        (
            AnalysisChannel(
                "ENGINEERING",
                ("Governance controls are implementable",),
                "adopt controls",
                "MEDIUM",
                ("REQ-ID-001",),
                (),
                "LOCAL_ENGINEERING",
                "STATIC_REVIEW",
            ),
            AnalysisChannel(
                "RESEARCH",
                ("Subjectivity remains unresolved",),
                "retain non-claim",
                "HIGH",
                ("STATUS_LOCK",),
                (),
                "RESEARCH_GOVERNANCE",
                "EVIDENCE_BOUNDARY",
            ),
        ),
        ("Canonical effect remains NONE",),
        ("Conceptual identity language is not engineering evidence",),
        ("Future research admission thresholds",),
    )
    write_new_json(ARTIFACTS / "perspectives" / f"{perspective.event_id}.json", perspective)
    event = LineageEvent(
        "LINEAGE-EVENT-000001",
        "GENESIS",
        "GENESIS",
        genesis.project_id,
        genesis.state_id,
        None,
        genesis.state_hash,
        "ENGINEERING_AGENT",
    )
    event_values = {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "previous_event_hash": event.previous_event_hash,
        "event_hash": event.expected_hash(),
        "project_id": event.project_id,
        "state_id": event.state_id,
        "fork_id": event.fork_id,
        "payload_hash": event.payload_hash,
        "actor_role": event.actor_role,
        "occurred_at": event.occurred_at,
        "approval_reference": event.approval_reference,
        "source_provenance": event.source_provenance,
        "notes": event.notes,
    }
    write_new_json(ARTIFACTS / "events" / "000001_GENESIS.json", event_values)
    print(ARTIFACTS)


if __name__ == "__main__":
    main()
