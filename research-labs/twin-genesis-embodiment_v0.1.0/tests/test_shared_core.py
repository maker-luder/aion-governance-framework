from __future__ import annotations

import importlib
import importlib.util
import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_twin_embodiment.models import EmbodimentTemplate
from aion_astra_twin_embodiment.shared_core import (
    ObservationDomain,
    build_shared_embodiment_core,
    shared_embodiment_core_hash,
    validate_shared_embodiment_core,
)


ROOT = Path(__file__).parents[1]
SCHEMA_PATH = ROOT / "schemas" / "SHARED_EMBODIMENT_CORE_SCHEMA.json"

REQUIRED_SURFACE = (
    "ObservationDomain",
    "ObservabilityClass",
    "StaticBodyRegion",
    "ObservationInterface",
    "MotorInterface",
    "PhysiologySystemInterface",
    "SharedEmbodimentCore",
    "build_shared_embodiment_core",
    "shared_embodiment_core_hash",
    "validate_shared_embodiment_core",
)


def test_shared_core_module_and_public_surface_exist() -> None:
    spec = importlib.util.find_spec("aion_astra_twin_embodiment.shared_core")
    assert spec is not None, "shared_core module must exist"
    module = importlib.import_module("aion_astra_twin_embodiment.shared_core")
    missing = [name for name in REQUIRED_SURFACE if not hasattr(module, name)]
    assert missing == [], f"missing shared-core surface: {missing}"


def test_shared_core_schema_exists() -> None:
    assert SCHEMA_PATH.is_file(), "shared-core schema must exist"


def test_shared_core_builds_role_neutral_region_and_signal_interfaces() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    core = build_shared_embodiment_core(template)
    assert {"LEFT_ARM", "RIGHT_ARM", "TORSO"} <= {
        region.region_id for region in core.body_regions
    }
    assert {ObservationDomain.PROPRIOCEPTIVE, ObservationDomain.VESTIBULAR} <= {
        interface.domain for interface in core.observation_interfaces
    }
    assert core.teacher_extension_required is False
    assert core.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert validate_shared_embodiment_core(core, template)["result"] == "PASS"


def test_shared_core_rejects_role_dependency_and_mismatched_template() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    core = build_shared_embodiment_core(template)
    with pytest.raises(ValueError, match="role-specific"):
        validate_shared_embodiment_core(
            replace(core, dependency_ids=("CHATGPT_TEACHER_ANTHROPOMETRY",)),
            template,
        )
    with pytest.raises(ValueError, match="template"):
        validate_shared_embodiment_core(
            core, EmbodimentTemplate("other-template", "v0.1")
        )


def test_shared_core_rejects_raw_enum_duplicate_region_and_missing_component() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    core = build_shared_embodiment_core(template)
    with pytest.raises(ValueError, match="enum"):
        validate_shared_embodiment_core(
            replace(core, observation_interfaces=(
                replace(core.observation_interfaces[0], domain="SOMATOSENSORY"),
                *core.observation_interfaces[1:],
            )),
            template,
        )
    with pytest.raises(ValueError, match="duplicate"):
        validate_shared_embodiment_core(
            replace(core, body_regions=(*core.body_regions, core.body_regions[0])),
            template,
        )
    with pytest.raises(ValueError, match="require"):
        validate_shared_embodiment_core(
            replace(core, motor_interfaces=()), template
        )


def test_shared_core_rejects_claim_promotion_and_invalid_motor_target() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    core = build_shared_embodiment_core(template)
    for changed in (
        replace(core, subjectivity_conclusion="ESTABLISHED"),
        replace(core, canonical_effect="MERGE"),
        replace(core, deployment=True),
    ):
        with pytest.raises(ValueError):
            validate_shared_embodiment_core(changed, template)
    with pytest.raises(ValueError, match="target"):
        validate_shared_embodiment_core(
            replace(core, motor_interfaces=(
                replace(core.motor_interfaces[0], target_region_ids=("UNKNOWN",)),
                *core.motor_interfaces[1:],
            )),
            template,
        )


def test_shared_core_schema_matches_record_and_rejects_unknown_properties() -> None:
    core = build_shared_embodiment_core(EmbodimentTemplate("adult-template", "v0.1"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(json.dumps(asdict(core)))
    assert not list(validator.iter_errors(payload))
    assert list(validator.iter_errors({**payload, "unexpected": True}))
    assert list(validator.iter_errors({**payload, "deployment": True}))
    assert list(validator.iter_errors({**payload, "body_regions": []}))


def test_shared_core_hash_is_reproducible_and_sensitive_to_core_content() -> None:
    template = EmbodimentTemplate("adult-template", "v0.1")
    first = build_shared_embodiment_core(template)
    second = build_shared_embodiment_core(template)
    assert shared_embodiment_core_hash(first) == shared_embodiment_core_hash(second)
    assert shared_embodiment_core_hash(first) != shared_embodiment_core_hash(
        replace(first, core_id="another-core")
    )
