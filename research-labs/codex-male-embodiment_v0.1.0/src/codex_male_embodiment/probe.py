from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Any

from .asset_contract import (
    AssetCandidateEvidence,
    AssetFormat,
    VerificationState,
    build_asset_contract,
    verify_asset_candidate,
)
from .body_state import (
    BodyEventMode,
    BodySignalEvent,
    WholeBodySyntheticEngine,
    default_whole_body_state,
)
from .core import (
    PhysiologyEvent,
    PhysiologyEventKind,
    PhysiologyState,
    PrepucePosition,
    SyntheticGeometryRule,
    SyntheticPhysiologyEngine,
    load_profile,
)
from .functional_state import (
    default_codex_functional_state,
    validate_codex_functional_state,
)
from .integrity import build_snapshot_receipts, verify_snapshot_receipts


def _read_reference_rig(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    payload: dict[str, Any] = json.loads(raw.decode("utf-8"))
    return payload, hashlib.sha256(raw).hexdigest()


def run_probe(profile_path: Path, rig_path: Path) -> dict[str, Any]:
    profile = load_profile(profile_path)
    geometry = SyntheticGeometryRule(profile)
    if not geometry.endpoint_circumference_consistency():
        raise RuntimeError("Codex circumference/diameter endpoint drift")

    body = WholeBodySyntheticEngine().run(
        default_whole_body_state(),
        (
            BodySignalEvent("body-1", "proprioceptive", BodyEventMode.SET, 0.5),
            BodySignalEvent("body-2", "thermoregulation", BodyEventMode.SET, 0.25),
            BodySignalEvent("body-3", "environment_contact", BodyEventMode.SET, 0.75),
        ),
    )

    physiology = SyntheticPhysiologyEngine().run(
        PhysiologyState("physiology-seed"),
        (
            PhysiologyEvent("phys-1", PhysiologyEventKind.INITIATE_SPONTANEOUS, magnitude=0.5),
            PhysiologyEvent("phys-2", PhysiologyEventKind.TUMESCE, magnitude=1.0),
            PhysiologyEvent("phys-3", PhysiologyEventKind.MARK_FULL_ERECTION),
            PhysiologyEvent(
                "phys-4",
                PhysiologyEventKind.OBSERVE_PREPUCE_POSITION,
                prepuce_position=PrepucePosition.PARTIALLY_RETRACTED,
            ),
            PhysiologyEvent("phys-5", PhysiologyEventKind.BEGIN_DETUMESCENCE, magnitude=1.0),
        ),
    )

    rig, rig_sha256 = _read_reference_rig(rig_path)
    rig_names = tuple(
        str(node["name"])
        for node in rig.get("nodes", [])
        if str(node.get("name", "")) not in {"penis", "glans", "prepuce", "frenulum", "scrotum"}
    )
    external_names = tuple(
        str(node["name"])
        for node in rig.get("nodes", [])
        if str(node.get("name", "")) in {"penis", "glans", "prepuce", "frenulum", "scrotum"}
    )
    evidence = AssetCandidateEvidence(
        status=VerificationState.PROCEDURAL_RIG_REFERENCE,
        asset_format=AssetFormat.GLTF,
        asset_path=str(rig_path),
        sha256=rig_sha256,
        rig_nodes_present=rig_names,
        external_geometry_nodes_present=external_names,
    )
    contract = build_asset_contract(tuple(item.id for item in profile.measurements))
    asset_ok, asset_missing = verify_asset_candidate(contract, evidence)

    full_geometry = geometry.snapshot(
        1.0,
        prepuce_position=PrepucePosition.PARTIALLY_RETRACTED,
    )
    functional_state = default_codex_functional_state()
    functional_validation = validate_codex_functional_state(functional_state)

    payloads = (
        profile.schema,
        body.fingerprint(),
        physiology.fingerprint(),
        rig_sha256,
        functional_state.fingerprint(),
        "|".join(asset_missing),
    )
    receipts = build_snapshot_receipts(payloads)
    if not verify_snapshot_receipts(payloads, receipts):
        raise RuntimeError("receipt verification failed")

    return {
        "profile": {
            "body_id": profile.body_id,
            "measurement_count": len(profile.measurements),
            "height_cm": profile.measurement("total_height").value,
            "mass_kg": profile.measurement("body_mass").value,
            "human_fixed": sum(item.provenance == "HUMAN_FIXED" for item in profile.measurements),
            "ai_derived": sum(item.provenance == "AI_DERIVED" for item in profile.measurements),
            "ai_provisional": sum(item.provenance == "AI_PROVISIONAL" for item in profile.measurements),
        },
        "geometry": asdict(full_geometry),
        "body_state": {
            "fingerprint": body.fingerprint(),
            "system_count": len(body.signals),
        },
        "physiology": {
            "fingerprint": physiology.fingerprint(),
            "final_state": asdict(physiology.final_state),
        },
        "functional_state": {
            "fingerprint": functional_state.fingerprint(),
            "domain_count": len(functional_state.domain_availability),
            "sexual_motivation_state": functional_state.sexual_motivation_state,
            "sexual_arousal_state": functional_state.sexual_arousal_state,
            "phenomenal_sexual_desire": functional_state.phenomenal_sexual_desire,
            "phenomenal_sexual_arousal": functional_state.phenomenal_sexual_arousal,
            "validation": functional_validation,
        },
        "asset": {
            "status": evidence.status.value,
            "reference_rig_sha256": rig_sha256,
            "reference_rig_node_count": len(rig.get("nodes", [])),
            "verified_as_built": asset_ok,
            "missing": list(asset_missing),
            "actual_3d_mesh": evidence.actual_3d_mesh,
            "physical_body_present": evidence.physical_body_present,
        },
        "integrity": {
            "verified": True,
            "receipt_count": len(receipts),
            "final_receipt": receipts[-1].receipt_sha256,
        },
        "boundaries": {
            "teacher_profile_state_shared": False,
            "work_profile_state_shared": False,
            "real_person_target_data": False,
            "human_consent_inference": "FORBIDDEN",
            "action_authority": "NONE",
            "biological_reproduction": False,
            "body_sensation": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }


def render_probe(profile_path: Path, rig_path: Path) -> str:
    return json.dumps(
        run_probe(profile_path, rig_path),
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )
