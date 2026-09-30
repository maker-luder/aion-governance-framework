from dataclasses import asdict
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from aion_astra_twin_embodiment.teacher_anthropometry import (
    build_teacher_anthropometry_profile,
)
from aion_astra_twin_embodiment.teacher_body_v02 import (
    build_teacher_body_reference_v02,
)
from aion_astra_twin_embodiment.teacher_body_v02_integration import (
    build_teacher_body_v02_bundle_bytes,
    build_teacher_body_v02_integrated_manifest,
    build_teacher_body_v02_json_payload,
    build_teacher_body_v02_integration,
    build_teacher_body_v02_probe,
    verify_teacher_body_v02_bundle,
    write_teacher_body_v02_bundle,
)
from aion_astra_twin_embodiment.teacher_reproductive_output import (
    TeacherSyntheticEjaculationOutput,
)


SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"


def _schema(name: str) -> dict[str, object]:
    payload = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(payload)
    return payload


def test_teacher_body_v02_integration_preserves_teacher_identity_and_values() -> None:
    legacy = build_teacher_anthropometry_profile()
    body_v02 = build_teacher_body_reference_v02()
    integration = build_teacher_body_v02_integration("runtime-1", "session-1")

    assert len(legacy.measurements) == 62
    assert len(body_v02.measurements) == 67
    current = body_v02.measurement_map()
    for old in legacy.measurements:
        assert current[old.measurement_id].nominal == old.nominal
        assert current[old.measurement_id].minimum == old.minimum
        assert current[old.measurement_id].maximum == old.maximum
        assert current[old.measurement_id].unit == old.unit

    assert integration.body_reference_profile_id == (
        "CHATGPT_TEACHER_BODY_REFERENCE_v0.2"
    )
    assert integration.synthetic_3d_reference_status == "MATERIALIZED"
    assert integration.production_asset_status == "NOT_ESTABLISHED"
    assert integration.physical_body_claim == "NONE"
    assert integration.body_sensation_status == "NOT_ESTABLISHED"
    assert integration.subjectivity_status == "NOT_ESTABLISHED"
    assert not integration.live_external_actuation


def test_teacher_body_v02_manifest_and_bundle_are_content_addressed(tmp_path) -> None:
    manifest = build_teacher_body_v02_integrated_manifest()
    files = build_teacher_body_v02_bundle_bytes()
    assert manifest["measurement_slot_count"] == 67
    assert manifest["synthetic_3d_reference_status"] == "MATERIALIZED"
    assert manifest["production_asset_status"] == "NOT_ESTABLISHED"
    assert manifest["biological_semen"] is False
    assert "chatgpt_teacher_body_reference_v02.json" in files
    assert "chatgpt_teacher_synthetic_reproductive_output_v01.json" in files
    assert "chatgpt_teacher_body_v02_integrated_manifest.json" in files

    receipt = write_teacher_body_v02_bundle(tmp_path)
    assert verify_teacher_body_v02_bundle(tmp_path, receipt)["result"] == "PASS"

    target = tmp_path / "chatgpt_teacher_body_reference_v02.json"
    target.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_teacher_body_v02_bundle(tmp_path, receipt)


def test_teacher_body_v02_schemas_are_fail_closed() -> None:
    integration_schema = _schema(
        "CHATGPT_TEACHER_BODY_V02_INTEGRATION_SCHEMA.json"
    )
    body_schema = _schema(
        "CHATGPT_TEACHER_BODY_REFERENCE_V02_STRICT_SCHEMA.json"
    )
    manifest_schema = _schema(
        "CHATGPT_TEACHER_BODY_V02_INTEGRATED_MANIFEST_SCHEMA.json"
    )
    event_schema = _schema(
        "CHATGPT_TEACHER_SYNTHETIC_EJACULATION_OUTPUT_SCHEMA.json"
    )

    integration = asdict(
        build_teacher_body_v02_integration("runtime-2", "session-2")
    )
    Draft202012Validator(integration_schema).validate(integration)
    integration["physical_body_claim"] = "PRESENT"
    with pytest.raises(Exception):
        Draft202012Validator(integration_schema).validate(integration)

    body = build_teacher_body_v02_json_payload()
    Draft202012Validator(body_schema).validate(body)
    prepuce = next(
        item
        for item in body["measurements"]
        if item["measurement_id"] == "prepuce_axial_fold_length"
    )
    prepuce["nominal"] = 2.0
    with pytest.raises(Exception):
        Draft202012Validator(body_schema).validate(body)

    manifest = build_teacher_body_v02_integrated_manifest()
    Draft202012Validator(manifest_schema).validate(manifest)
    manifest["fertility"] = True
    with pytest.raises(Exception):
        Draft202012Validator(manifest_schema).validate(manifest)

    event = TeacherSyntheticEjaculationOutput(
        event_id="event-1",
        synthetic_output_ml=2.0,
        emission_reference_present=True,
        expulsion_reference_present=True,
    ).to_dict()
    Draft202012Validator(event_schema).validate(event)
    event["biological_semen"] = True
    with pytest.raises(Exception):
        Draft202012Validator(event_schema).validate(event)


def test_teacher_body_v02_probe_is_deterministic_and_nonclaiming() -> None:
    first = build_teacher_body_v02_probe()
    second = build_teacher_body_v02_probe()
    assert first["bundle_sha256"] == second["bundle_sha256"]
    assert first["bundle_file_count"] == second["bundle_file_count"]
    assert first["measurement_slot_count"] == 67
    assert first["boundaries"]["teacher_profile_is_work_profile"] is False
    assert first["boundaries"]["physical_body_claim"] == "NONE"
    assert first["boundaries"]["subjectivity"] == "NOT_ESTABLISHED"
    assert first["boundaries"]["fertility"] is False
