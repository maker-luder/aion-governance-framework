from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from work_male_embodiment.capability import (
    TRANSFERABLE_CAPABILITIES,
    WORK_BODY_ID,
    build_work_capability_record,
    validate_work_capability_record,
)
from work_male_embodiment.continuity import (
    build_adaptation_state,
    build_body_runtime_binding,
    build_calibration_state,
    build_cross_session_retention,
    capture_session_snapshot,
    observe_longitudinal,
)
from work_male_embodiment.core import load_profile


REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "docs/research/embodiment/WORK_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"


def _snapshot(session_id: str, sequence: int, stride_gain: float):
    profile = load_profile(PROFILE)
    binding = build_body_runtime_binding("work-reference-runtime", session_id)
    calibration = build_calibration_state(
        binding,
        profile,
        observed={
            "total_height": 165.0,
            "biacromial_shoulder_breadth": 47.0,
        },
    )
    adaptation = build_adaptation_state(
        calibration,
        sequence=sequence,
        parameter_offsets={"stride_gain": stride_gain},
    )
    return capture_session_snapshot(calibration, adaptation)


def test_work_transferable_capability_surface_keeps_work_body_distinct() -> None:
    profile = load_profile(PROFILE)
    record = build_work_capability_record(profile)
    result = validate_work_capability_record(record)
    assert record.body_id == WORK_BODY_ID
    assert len(record.capabilities) == len(TRANSFERABLE_CAPABILITIES) == 18
    assert result["result"] == "PASS"
    assert record.shared_mutable_state is False
    assert record.shared_history is False
    assert record.shared_identity is False


def test_capability_record_rejects_phenomenal_promotion() -> None:
    profile = load_profile(PROFILE)
    record = build_work_capability_record(profile)
    with pytest.raises(ValueError, match="phenomenal"):
        replace(record, subjectivity="ESTABLISHED")


def test_cross_session_retention_and_longitudinal_observation_are_bounded() -> None:
    snapshots = (
        _snapshot("session-1", 0, 0.0),
        _snapshot("session-2", 1, 0.05),
        _snapshot("session-3", 2, 0.05),
    )
    retention = build_cross_session_retention(snapshots)
    observation = observe_longitudinal(retention)
    assert observation.change_status == "OBSERVED_CROSS_SESSION_CHANGE"
    assert observation.changed_parameters == ("stride_gain",)
    assert observation.persistent_changed_parameters == ("stride_gain",)
    assert observation.developmental_mechanism == "NOT_ESTABLISHED"
    assert retention.identity_continuity_claim == "NONE"
    assert retention.subjective_continuity == "NOT_ESTABLISHED"


def test_retention_schema_accepts_work_payload_and_rejects_identity_claim() -> None:
    retention = build_cross_session_retention(
        (_snapshot("session-schema", 0, 0.0),)
    )
    schema = json.loads(
        (PACKAGE_ROOT / "schemas/work_continuity_v0.1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    payload = json.loads(json.dumps(asdict(retention)))
    Draft202012Validator(schema).validate(payload)
    payload["identity_continuity_claim"] = "ESTABLISHED"
    with pytest.raises(Exception):
        Draft202012Validator(schema).validate(payload)
