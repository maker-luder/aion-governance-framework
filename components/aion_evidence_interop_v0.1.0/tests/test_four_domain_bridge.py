from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from aion_evidence_interop.canonical import InteropError, canonical_json_bytes
from aion_evidence_interop.four_domain_bridge import (
    FOUR_DOMAIN_SOURCE_ARTIFACT,
    FOUR_DOMAIN_SOURCE_BLOB_SHA1,
    FOUR_DOMAIN_SOURCE_HEAD,
    exact_source_url,
    materialize_four_domain_record,
    materialize_four_domain_record_bytes,
    validate_four_domain_descriptor,
)
from aion_evidence_interop.manifest import build_bundle


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]
DESCRIPTOR = COMPONENT / "fixtures" / "four_domain_snapshot_descriptor.json"
RECORD = COMPONENT / "fixtures" / "four_domain_snapshot_record.json"
DESCRIPTOR_SCHEMA = COMPONENT / "schemas" / "four_domain_bridge_descriptor_v0.1.0.schema.json"
EVIDENCE_SCHEMA = ROOT / "schemas" / "research_evidence_record_v0.2.0.schema.json"


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_descriptor_is_closed_and_pinned_to_frozen_four_domain_source() -> None:
    schema = _load(DESCRIPTOR_SCHEMA)
    value = _load(DESCRIPTOR)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(value)

    assert value["source_head"] == FOUR_DOMAIN_SOURCE_HEAD
    assert value["source_artifact"] == {
        "path": FOUR_DOMAIN_SOURCE_ARTIFACT,
        "git_blob_sha1": FOUR_DOMAIN_SOURCE_BLOB_SHA1,
    }


def test_descriptor_schema_rejects_source_head_or_blob_drift() -> None:
    schema = _load(DESCRIPTOR_SCHEMA)
    for path, invalid in (
        (("source_head",), "0" * 40),
        (("source_artifact", "git_blob_sha1"), "1" * 40),
    ):
        value = deepcopy(_load(DESCRIPTOR))
        target = value
        for part in path[:-1]:
            target = target[part]  # type: ignore[assignment,index]
        target[path[-1]] = invalid  # type: ignore[index]
        with pytest.raises(ValidationError):
            Draft202012Validator(schema).validate(value)


def test_runtime_descriptor_validation_fails_closed_on_drift() -> None:
    value = _load(DESCRIPTOR)
    validate_four_domain_descriptor(value)

    changed = deepcopy(value)
    changed["source_head"] = "0" * 40
    with pytest.raises(InteropError) as caught:
        validate_four_domain_descriptor(changed)
    assert caught.value.category == "bridge_descriptor_failure"

    changed = deepcopy(value)
    changed["source_artifact"]["path"] = "../private.md"  # type: ignore[index]
    with pytest.raises(InteropError) as caught:
        validate_four_domain_descriptor(changed)
    assert caught.value.category == "bridge_descriptor_failure"


def test_materialized_record_matches_committed_fixture_and_aion_schema() -> None:
    descriptor = _load(DESCRIPTOR)
    generated = materialize_four_domain_record(ROOT, descriptor)
    fixture = _load(RECORD)

    assert canonical_json_bytes(generated) == canonical_json_bytes(fixture)

    schema = _load(EVIDENCE_SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(generated)


def test_bridge_preserves_hold_and_nonclaim_boundaries() -> None:
    record = materialize_four_domain_record(ROOT, _load(DESCRIPTOR))
    assert record["code_commit"] == FOUR_DOMAIN_SOURCE_HEAD
    assert record["result_status"] == "HOLD"
    assert record["canonical_effect"] == "NONE"
    assert record["independent_validation_status"] == "IVV_NOT_ACHIEVED"

    nonclaims = record["nonclaims"]
    assert nonclaims["main_effect"] == "NONE"
    assert nonclaims["canonical_effect"] == "NONE"
    assert nonclaims["live_runtime_effect"] == "NONE"
    assert nonclaims["runtime_effect"] == "NONE"
    assert nonclaims["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert nonclaims["consciousness_conclusion"] == "NOT_ESTABLISHED"
    assert nonclaims["identity_continuity_conclusion"] == "NOT_ESTABLISHED"


def test_bridge_uses_exact_commit_source_url_without_live_branch_lookup() -> None:
    url = exact_source_url()
    assert f"/blob/{FOUR_DOMAIN_SOURCE_HEAD}/" in url
    assert FOUR_DOMAIN_SOURCE_ARTIFACT in url
    assert "/blob/review/four-domain-research-materialization/" not in url


def test_bridge_generation_is_byte_deterministic() -> None:
    descriptor = _load(DESCRIPTOR)
    first = materialize_four_domain_record_bytes(ROOT, descriptor)
    second = materialize_four_domain_record_bytes(ROOT, deepcopy(descriptor))
    assert first == second


def test_committed_bridge_record_flows_through_all_interop_outputs() -> None:
    bundle = build_bundle(ROOT, RECORD, expected_head=_head())
    assert set(bundle) == {
        "interop-manifest.json",
        "prov.jsonld",
        "attestation.intoto.json",
        "ro-crate-metadata.json",
        "opa/input.json",
        "inspect/task-manifest.json",
        "inspect/dataset.jsonl",
        "openssf/scorecard-crosswalk.json",
    }

    manifest = json.loads(bundle["interop-manifest.json"])
    assert manifest["source"]["validation_status"] == "PASS"
    assert manifest["source"]["result_status"] == "HOLD"
    assert manifest["boundaries"]["canonical_effect"] == "NONE"
    assert manifest["boundaries"]["research_execution"] is False
    assert manifest["boundaries"]["model_execution"] is False
    assert manifest["boundaries"]["network_access"] is False


def test_source_commit_remains_inside_hash_bound_record_material() -> None:
    record_bytes = RECORD.read_bytes()
    assert FOUR_DOMAIN_SOURCE_HEAD.encode("ascii") in record_bytes
    assert FOUR_DOMAIN_SOURCE_BLOB_SHA1.encode("ascii") in record_bytes

    bundle = build_bundle(ROOT, RECORD, expected_head=_head())
    intoto = json.loads(bundle["attestation.intoto.json"])
    source_material = intoto["predicate"]["materials"][0]
    assert source_material["uri"].endswith("four_domain_snapshot_record.json")
    assert len(source_material["digest"]["sha256"]) == 64
