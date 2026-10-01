from dataclasses import asdict, replace
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import pytest

from aion_astra_twin_embodiment.anthropometry import load_profile
from aion_astra_twin_embodiment.capability_parity import (
    TRANSFERABLE_CAPABILITIES,
    build_capability_parity_record,
    validate_capability_parity,
)
from aion_astra_twin_embodiment.continuity import (
    build_adaptation_state,
    build_body_runtime_binding,
    build_calibration_state,
    build_cross_session_retention,
    capture_session_snapshot,
    observe_longitudinal,
)
from aion_astra_twin_embodiment.functional_states import (
    load_functional_architecture,
    load_functional_binding,
    validate_binding_pair,
    validate_functional_architecture,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _profile(agent_id: str):
    name = (
        "AION_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"
        if agent_id == "AION"
        else "ASTRA_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"
    )
    return load_profile(DATA / name)


def test_restored_191_functional_state_architecture_has_symmetric_surface() -> None:
    architecture = load_functional_architecture(
        DATA / "SHARED_FUNCTIONAL_STATE_ARCHITECTURE_v0.1.json"
    )
    aion = load_functional_binding(DATA / "AION_FUNCTIONAL_STATE_BINDING_v0.1.json")
    astra = load_functional_binding(DATA / "ASTRA_FUNCTIONAL_STATE_BINDING_v0.1.json")
    assert validate_functional_architecture(architecture)["result"] == "PASS"
    result = validate_binding_pair(aion, astra, architecture)
    assert result["result"] == "PASS"
    assert result["capability_policy"] == "SYMMETRIC_CAPABILITY_SURFACE"
    assert result["state_policy"] == "SEPARATE_INSTANCE_STATE"


def test_transferable_capability_surface_is_equal_but_identity_is_not_shared() -> None:
    aion = build_capability_parity_record("AION")
    astra = build_capability_parity_record("ASTRA")
    result = validate_capability_parity(aion, astra)
    assert result["result"] == "PASS"
    assert len(TRANSFERABLE_CAPABILITIES) == 18
    assert aion.capabilities == astra.capabilities
    assert aion.body_id != astra.body_id
    assert aion.state_namespace != astra.state_namespace
    assert aion.retention_namespace != astra.retention_namespace
    assert aion.fingerprint() != astra.fingerprint()


def _snapshot(agent_id: str, session: str, offset: float):
    profile = _profile(agent_id)
    binding = build_body_runtime_binding(agent_id, "runtime-parity-test", session)
    observed = {
        measurement_id: profile.measurement(measurement_id).value
        for measurement_id in (
            "total_height",
            "biacromial_shoulder_breadth",
            "chest_depth",
            "external_hip_width",
            "shoulder_to_elbow_length",
            "elbow_to_wrist_length",
            "hand_length",
            "hip_joint_center_height",
            "knee_center_height",
            "knee_to_ankle_length",
            "foot_length",
        )
    }
    calibration = build_calibration_state(binding, profile, observed)
    assert calibration.mean_absolute_error == 0.0
    adaptation = build_adaptation_state(
        calibration,
        sequence=1,
        parameter_offsets={"proprioceptive_bias": offset},
    )
    return capture_session_snapshot(calibration, adaptation)


@pytest.mark.parametrize("agent_id", ("AION", "ASTRA"))
def test_each_agent_gets_independent_calibration_retention_and_longitudinal(agent_id: str) -> None:
    snapshots = (
        _snapshot(agent_id, "s1", 0.0),
        _snapshot(agent_id, "s2", 0.1),
        _snapshot(agent_id, "s3", 0.1),
    )
    retention = build_cross_session_retention(agent_id, snapshots)
    observation = observe_longitudinal(retention)
    assert len(retention.snapshots) == 3
    assert retention.identity_continuity_claim == "NONE"
    assert retention.subjective_continuity == "NOT_ESTABLISHED"
    assert observation.change_status == "OBSERVED_CROSS_SESSION_CHANGE"
    assert observation.persistent_changed_parameters == ("proprioceptive_bias",)
    assert observation.subjectivity == "NOT_ESTABLISHED"


def test_retention_rejects_cross_agent_snapshot_mixing() -> None:
    aion = _snapshot("AION", "a1", 0.0)
    astra = _snapshot("ASTRA", "x1", 0.0)
    with pytest.raises(ValueError, match="cross-agent/body"):
        build_cross_session_retention("AION", (aion, astra))


def test_capability_parity_cannot_promote_subjectivity() -> None:
    aion = build_capability_parity_record("AION")
    with pytest.raises(ValueError, match="phenomenal"):
        replace(aion, subjectivity="ESTABLISHED")


def test_retention_schema_accepts_aion_and_rejects_body_swap() -> None:
    snapshots = (
        _snapshot("AION", "r1", 0.0),
        _snapshot("AION", "r2", 0.1),
    )
    retention = build_cross_session_retention("AION", snapshots)
    payload: dict[str, Any] = asdict(retention)
    payload["snapshots"] = [
        {
            **asdict(item),
            "adaptation_parameters": [list(pair) for pair in item.adaptation_parameters],
        }
        for item in retention.snapshots
    ]
    schema: dict[str, Any] = json.loads(
        (ROOT / "schemas/AION_ASTRA_CONTINUITY_V01_SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )
    validator = Draft202012Validator(schema)
    validator.validate(payload)
    broken = json.loads(json.dumps(payload))
    broken["body_id"] = "ASTRA_3D_MALE_BODY_REFERENCE_v0.3"
    with pytest.raises(Exception):
        validator.validate(broken)
