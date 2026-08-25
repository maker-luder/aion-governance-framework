from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

from aion_astra_agent_substrate import (
    RuntimeBinding,
    dsh_profile,
    materialize_research_evidence_bytes,
    materialize_research_evidence_record,
    normalize_dsh_trajectory,
)


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]
FIXTURE = COMPONENT / "fixtures/dsh_session_events.json"
EVIDENCE_SCHEMA = ROOT / "schemas/research_evidence_record_v0.2.0.schema.json"


def _head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def _binding() -> RuntimeBinding:
    return RuntimeBinding.from_runtime_context(
        {
            "agent_id": "AION",
            "runtime_instance_id": "AION-I-001",
            "memory_stream_id": "AION-MEM-001",
            "event_lineage_id": "AION-EVT-001",
            "canonical_state_reference": "AION-CANONICAL",
            "genesis_root_id": "GENESIS-001",
        },
        substrate_id="dsh-pinned",
        session_id="dsh-aion-session-001",
    )


def _record() -> dict[str, object]:
    events = json.loads(FIXTURE.read_text(encoding="utf-8"))
    normalized = normalize_dsh_trajectory(events, binding=_binding())
    return materialize_research_evidence_record(
        ROOT,
        binding=_binding(),
        profile=dsh_profile(),
        events=normalized,
        code_commit=_head(),
        claim_id="agent-substrate-dsh-fixture-001",
    )


def test_trajectory_materializes_valid_research_evidence_record() -> None:
    record = _record()
    schema = json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(record)
    assert record["result_status"] == "HOLD"
    assert record["canonical_effect"] == "NONE"
    assert record["independent_validation_status"] == "IVV_NOT_ACHIEVED"


def test_trajectory_record_preserves_nonclaims() -> None:
    nonclaims = _record()["nonclaims"]
    assert nonclaims["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert nonclaims["consciousness_conclusion"] == "NOT_ESTABLISHED"
    assert nonclaims["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
    assert nonclaims["main_effect"] == "NONE"
    assert nonclaims["runtime_effect"] == "NONE"


def test_materialized_record_bytes_are_deterministic() -> None:
    events = json.loads(FIXTURE.read_text(encoding="utf-8"))
    normalized = normalize_dsh_trajectory(events, binding=_binding())
    kwargs = dict(
        root=ROOT,
        binding=_binding(),
        profile=dsh_profile(),
        events=normalized,
        code_commit=_head(),
        claim_id="agent-substrate-dsh-fixture-001",
    )
    assert materialize_research_evidence_bytes(**kwargs) == materialize_research_evidence_bytes(**kwargs)


def test_trajectory_record_flows_through_existing_evidence_interop() -> None:
    from aion_evidence_interop.manifest import build_bundle

    record_path = COMPONENT / "fixtures" / "_generated_substrate_record.tmp.json"
    try:
        record_path.write_text(json.dumps(_record(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        bundle = build_bundle(ROOT, record_path, expected_head=_head())
    finally:
        record_path.unlink(missing_ok=True)
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
    assert manifest["boundaries"]["model_execution"] is False
    assert manifest["boundaries"]["network_access"] is False
