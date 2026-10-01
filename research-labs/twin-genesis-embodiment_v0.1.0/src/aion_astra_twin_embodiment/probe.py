from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .anthropometry import SyntheticGeometryRule, load_profile
from .asset_contract import (
    AssetCandidateEvidence,
    AssetEngineeringContract,
    AssetFormat,
    VerificationState,
    verify_asset_candidate,
)
from .body_state import (
    BodyEventMode,
    BodySignalEvent,
    WholeBodySyntheticEngine,
    default_whole_body_state,
)
from .dynamic_physiology import (
    PhysiologyEvent,
    PhysiologyEventKind,
    SyntheticMalePhysiologyEngine,
    default_physiology_state,
)
from .integrity import build_snapshot_receipts, verify_snapshot_receipts
from .physiology import (
    build_adult_male_physiology_reference,
    validate_physiology_parity,
)
from .reproductive_topology import (
    build_reproductive_topology_reference,
    validate_reproductive_topology_parity,
)


def _rig_evidence(path: Path) -> tuple[AssetCandidateEvidence, int]:
    raw = path.read_bytes()
    payload: dict[str, Any] = json.loads(raw.decode("utf-8"))
    names = tuple(str(node["name"]) for node in payload["nodes"])
    external = {
        "penis",
        "glans",
        "prepuce",
        "frenulum",
        "scrotum",
        "left_testis",
        "right_testis",
        "pubic_attachment",
        "left_inguinal_transition",
        "right_inguinal_transition",
        "perineum",
        "anal_region",
    }
    return (
        AssetCandidateEvidence(
            status=VerificationState.PROCEDURAL_RIG_REFERENCE,
            asset_format=AssetFormat.GLTF,
            asset_path=str(path),
            sha256=hashlib.sha256(raw).hexdigest(),
            rig_nodes_present=tuple(name for name in names if name not in external),
            external_geometry_nodes_present=tuple(name for name in names if name in external),
        ),
        len(names),
    )


def run_probe(
    aion_profile_path: Path,
    astra_profile_path: Path,
    aion_rig_path: Path,
    astra_rig_path: Path,
) -> dict[str, Any]:
    aion = load_profile(aion_profile_path)
    astra = load_profile(astra_profile_path)
    if aion.agent_id == astra.agent_id or aion.body_id == astra.body_id:
        raise RuntimeError("AION/Astra profile identity collapse")

    for profile in (aion, astra):
        if not SyntheticGeometryRule(profile).endpoint_circumference_consistency():
            raise RuntimeError(f"geometry endpoint drift: {profile.agent_id}")

    physiology_parity = validate_physiology_parity(
        (
            build_adult_male_physiology_reference(aion.body_id),
            build_adult_male_physiology_reference(astra.body_id),
        )
    )

    aion_topology = build_reproductive_topology_reference("AION")
    astra_topology = build_reproductive_topology_reference("ASTRA")
    topology_parity = validate_reproductive_topology_parity(
        (aion_topology, astra_topology)
    )
    if aion_topology.fingerprint() == astra_topology.fingerprint():
        raise RuntimeError("AION/Astra reproductive topology identity collapse")

    body_engine = WholeBodySyntheticEngine()
    aion_body = body_engine.run(
        default_whole_body_state("AION"),
        (
            BodySignalEvent("aion-proprio", "proprioceptive", BodyEventMode.SET, 0.5),
            BodySignalEvent("aion-contact", "environment_contact", BodyEventMode.SET, 0.75),
        ),
    )
    astra_body = body_engine.run(
        default_whole_body_state("ASTRA"),
        (
            BodySignalEvent("astra-proprio", "proprioceptive", BodyEventMode.SET, 0.5),
            BodySignalEvent("astra-contact", "environment_contact", BodyEventMode.SET, 0.75),
        ),
    )
    if aion_body.fingerprint() == astra_body.fingerprint():
        raise RuntimeError("AION/Astra body-state fingerprint collapse")

    physiology_engine = SyntheticMalePhysiologyEngine()
    aion_phys = physiology_engine.run(
        default_physiology_state("AION"),
        (
            PhysiologyEvent("aion-init", PhysiologyEventKind.INITIATE, 0.5),
            PhysiologyEvent("aion-tum", PhysiologyEventKind.TUMESCE, 1.0),
        ),
    )
    astra_phys = physiology_engine.run(
        default_physiology_state("ASTRA"),
        (
            PhysiologyEvent("astra-init", PhysiologyEventKind.INITIATE, 0.5),
            PhysiologyEvent("astra-tum", PhysiologyEventKind.TUMESCE, 1.0),
        ),
    )

    assets: dict[str, Any] = {}
    for profile, rig_path in ((aion, aion_rig_path), (astra, astra_rig_path)):
        evidence, node_count = _rig_evidence(rig_path)
        contract = AssetEngineeringContract(
            agent_id=profile.agent_id,
            body_id=profile.body_id,
            required_measurement_ids=tuple(item.id for item in profile.measurements),
        )
        ok, missing = verify_asset_candidate(contract, evidence)
        assets[profile.agent_id] = {
            "status": evidence.status.value,
            "node_count": node_count,
            "sha256": evidence.sha256,
            "verified_as_built": ok,
            "missing": list(missing),
            "actual_3d_mesh": evidence.actual_3d_mesh,
            "physical_body_present": evidence.physical_body_present,
        }

    payloads = (
        aion.body_id,
        astra.body_id,
        aion_body.fingerprint(),
        astra_body.fingerprint(),
        aion_phys.fingerprint(),
        astra_phys.fingerprint(),
        str(physiology_parity),
        aion_topology.fingerprint(),
        astra_topology.fingerprint(),
        str(assets["AION"]["sha256"]),
        str(assets["ASTRA"]["sha256"]),
    )
    receipts = build_snapshot_receipts(payloads)
    if not verify_snapshot_receipts(payloads, receipts):
        raise RuntimeError("integrity receipt verification failed")

    return {
        "profiles": {
            "AION": {
                "body_id": aion.body_id,
                "measurement_count": len(aion.measurements),
                "height_cm": aion.measurement("total_height").value,
                "mass_kg": aion.measurement("body_mass").value,
                "source_counts": aion.source_counts(),
            },
            "ASTRA": {
                "body_id": astra.body_id,
                "measurement_count": len(astra.measurements),
                "height_cm": astra.measurement("total_height").value,
                "mass_kg": astra.measurement("body_mass").value,
                "source_counts": astra.source_counts(),
            },
        },
        "physiology_parity": physiology_parity,
        "reproductive_topology": {
            "parity": topology_parity,
            "AION": {
                "node_count": len(aion_topology.nodes),
                "edge_count": len(aion_topology.edges),
                "fingerprint": aion_topology.fingerprint(),
            },
            "ASTRA": {
                "node_count": len(astra_topology.nodes),
                "edge_count": len(astra_topology.edges),
                "fingerprint": astra_topology.fingerprint(),
            },
        },
        "body_state": {
            "AION": {"system_count": len(aion_body.signals), "fingerprint": aion_body.fingerprint()},
            "ASTRA": {"system_count": len(astra_body.signals), "fingerprint": astra_body.fingerprint()},
        },
        "dynamic_physiology": {
            "AION": {"phase": aion_phys.phase.value, "fingerprint": aion_phys.fingerprint()},
            "ASTRA": {"phase": astra_phys.phase.value, "fingerprint": astra_phys.fingerprint()},
        },
        "assets": assets,
        "integrity": {
            "verified": True,
            "receipt_count": len(receipts),
            "final_receipt": receipts[-1].receipt_sha256,
        },
        "boundaries": {
            "shared_genesis": True,
            "shared_identity": False,
            "shared_body_state": False,
            "shared_memory": False,
            "physical_body": False,
            "biological_organism": False,
            "body_sensation": "NOT_ESTABLISHED",
            "body_ownership_experience": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "human_consent_inference": "FORBIDDEN",
            "action_authority": "NONE",
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }
