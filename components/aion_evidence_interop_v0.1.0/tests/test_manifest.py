from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from aion_evidence_interop.canonical import InteropError
from aion_evidence_interop.manifest import build_bundle


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def test_bundle_is_deterministic_and_bounded() -> None:
    record = COMPONENT / "fixtures" / "valid_minimal.json"
    first = build_bundle(ROOT, record, expected_head=_head())
    second = build_bundle(ROOT, record, expected_head=_head())
    assert first == second

    manifest = json.loads(first["interop-manifest.json"])
    assert manifest["source"]["validation_status"] == "PASS"
    assert manifest["boundaries"]["canonical_effect"] == "NONE"
    assert manifest["boundaries"]["deployment"] is False
    assert manifest["boundaries"]["model_execution"] is False
    assert manifest["boundaries"]["network_access"] is False
    assert manifest["boundaries"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert manifest["policy"]["python_mirror_allow"] is True

    assert set(first) == {
        "interop-manifest.json",
        "prov.jsonld",
        "attestation.intoto.json",
        "ro-crate/ro-crate-metadata.json",
        "opa/input.json",
        "inspect/task-manifest.json",
        "inspect/dataset.jsonl",
    }


def test_completed_record_with_wrong_head_fails_closed() -> None:
    record = COMPONENT / "fixtures" / "invalid_head.json"
    with pytest.raises(InteropError, match="source evidence validation failed closed"):
        build_bundle(ROOT, record, expected_head=_head())


def test_invalid_canonical_effect_fails_closed() -> None:
    record = COMPONENT / "fixtures" / "invalid_canonical_effect.json"
    with pytest.raises(InteropError, match="source evidence validation failed closed"):
        build_bundle(ROOT, record, expected_head=_head())


def test_manifest_schema_freezes_critical_boundaries() -> None:
    schema = json.loads(
        (COMPONENT / "schemas" / "interop_manifest_v0.1.0.schema.json").read_text()
    )
    props = schema["properties"]["boundaries"]["properties"]
    assert props["canonical_effect"]["const"] == "NONE"
    assert props["deployment"]["const"] is False
    assert props["model_execution"]["const"] is False
    assert props["network_access"]["const"] is False
    assert props["subjectivity_conclusion"]["const"] == "NOT_ESTABLISHED"
