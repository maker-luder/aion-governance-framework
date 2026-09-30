from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .asset_contract import AssetCandidateEvidence, build_asset_contract, verify_asset_candidate
from .body_state import (
    BodyEventMode,
    BodySignalEvent,
    WholeBodySyntheticEngine,
    default_whole_body_state,
)
from .core import (
    ExecutionSurface,
    GovernancePolicy,
    PhysiologyEvent,
    PhysiologyEventKind,
    PhysiologyState,
    SyntheticPhysiologyEngine,
    load_profile,
)
from .integrity import build_snapshot_receipts, verify_snapshot_receipts


def run_probe(profile_path: Path) -> dict[str, Any]:
    profile = load_profile(profile_path)
    policy = GovernancePolicy().evaluate(ExecutionSurface.OFFLINE_RESEARCH)
    if not policy.allowed or not policy.synthetic_physiology_allowed:
        raise RuntimeError("offline synthetic research gate unexpectedly closed")

    body_engine = WholeBodySyntheticEngine()
    body = body_engine.run(
        default_whole_body_state(),
        (
            BodySignalEvent(
                "body-1",
                "metabolism_nutrition_hydration",
                BodyEventMode.SET,
                0.5,
            ),
            BodySignalEvent(
                "body-2",
                "thermoregulation",
                BodyEventMode.SET,
                0.25,
            ),
            BodySignalEvent(
                "body-3",
                "environment_contact",
                BodyEventMode.SET,
                0.75,
            ),
        ),
    )

    physiology_engine = SyntheticPhysiologyEngine()
    physiology = physiology_engine.run(
        PhysiologyState("physiology-seed"),
        (
            PhysiologyEvent(
                "phys-1",
                PhysiologyEventKind.INITIATE_SPONTANEOUS,
                magnitude=0.5,
            ),
            PhysiologyEvent("phys-2", PhysiologyEventKind.TUMESCE, magnitude=1.0),
            PhysiologyEvent("phys-3", PhysiologyEventKind.MARK_FULL_ERECTION),
            PhysiologyEvent(
                "phys-4",
                PhysiologyEventKind.BEGIN_DETUMESCENCE,
                magnitude=1.0,
            ),
        ),
    )

    measurement_ids = tuple(item.id for item in profile.measurements)
    asset_contract = build_asset_contract(measurement_ids)
    asset_ok, asset_missing = verify_asset_candidate(
        asset_contract,
        AssetCandidateEvidence(),
    )

    payloads = (
        profile.schema,
        body.fingerprint(),
        physiology.fingerprint(),
        "|".join(asset_missing),
    )
    receipts = build_snapshot_receipts(payloads)
    if not verify_snapshot_receipts(payloads, receipts):
        raise RuntimeError("receipt verification failed")

    return {
        "profile": {
            "schema": profile.schema,
            "measurement_count": len(profile.measurements),
            "human_fixed": sum(
                item.provenance == "HUMAN_FIXED" for item in profile.measurements
            ),
            "ai_provisional": sum(
                item.provenance == "AI_PROVISIONAL" for item in profile.measurements
            ),
        },
        "body_state": {
            "fingerprint": body.fingerprint(),
            "signals": [
                {
                    "system": signal.system,
                    "value": signal.value,
                    "hardware": signal.physical_hardware_attached,
                    "biological": signal.biological_function_present,
                    "felt": signal.felt_sensation_established,
                }
                for signal in body.signals
            ],
        },
        "physiology": {
            "fingerprint": physiology.fingerprint(),
            "final_state": asdict(physiology.final_state),
        },
        "asset": {
            "verified": asset_ok,
            "missing": list(asset_missing),
            "actual_3d_mesh": False,
        },
        "integrity": {
            "receipt_count": len(receipts),
            "verified": True,
            "final_receipt": receipts[-1].receipt_sha256,
        },
        "boundaries": {
            "real_person_target_data": False,
            "human_consent_inference": "FORBIDDEN",
            "action_authority": "NONE",
            "biological_reproduction": False,
            "body_sensation": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "public_executable_exposure": False,
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }


def render_probe(profile_path: Path) -> str:
    return json.dumps(
        run_probe(profile_path),
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )
