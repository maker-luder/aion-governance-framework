from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_research_evidence as validator  # noqa: E402


def _schema() -> dict[str, object]:
    return json.loads(
        (ROOT / "schemas" / "research_evidence_record_v0.2.0.schema.json").read_text(
            encoding="utf-8"
        )
    )


def _architecture(schema: dict[str, object]) -> dict[str, object]:
    properties = schema["properties"]
    assert isinstance(properties, dict)
    architecture_schema = properties["evidence_architecture"]
    assert isinstance(architecture_schema, dict)
    required = set(architecture_schema["required"])
    if "standing_inference_stage_ref" in required:
        return {
            "standing_inference_stage_ref": "whitepaper:v0.14.21:four-stage:mechanism",
            "dimension_ref": "whitepaper:v0.14.21:AB.6:causal-boundary",
            "alternative_explanation_refs": ["qa/alternative.json"],
            "causal_intervention_refs": ["qa/intervention.json"],
            "ablation_refs": [],
            "counterfactual_refs": ["qa/counterfactual.json"],
            "robustness_refs": [],
            "replication_refs": [],
            "provenance_refs": ["qa/provenance.json"],
            "admissibility_ref": "qa/admissibility.json",
            "claim_scope": "mechanism candidate only",
            "unresolved_gap_refs": ["qa/gap.json"],
            "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
            "inference_stage": "MECHANISM",
            "alternative_explanations": ["retrieval-context confound"],
        }
    return {
        "alternative_explanation_refs": ["qa/alternative.json"],
        "causal_intervention_refs": ["qa/intervention.json"],
        "ablation_refs": [],
        "counterfactual_refs": ["qa/counterfactual.json"],
        "robustness_refs": [],
        "replication_refs": [],
        "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
        "inference_stage": "MECHANISM",
        "observation": "The bounded output occurred under the recorded protocol.",
        "mechanism": "The measured state changed under the governed intervention.",
        "interpretation": "The result remains compatible with a mechanism candidate and non-subjective alternatives.",
        "alternative_explanations": ["retrieval-context confound"],
        "provenance_refs": ["qa/provenance.json"],
        "admissibility_ref": "qa/admissibility.json",
        "claim_scope": "mechanism candidate only",
        "unresolved_gap_refs": ["qa/gap.json"],
    }


def _nonclaims(schema: dict[str, object]) -> dict[str, str]:
    properties = schema["properties"]
    assert isinstance(properties, dict)
    block = properties["nonclaims"]
    assert isinstance(block, dict)
    block_properties = block["properties"]
    assert isinstance(block_properties, dict)
    result: dict[str, str] = {}
    for key, definition in block_properties.items():
        assert isinstance(definition, dict) and "const" in definition
        result[str(key)] = str(definition["const"])
    return result


def valid_record(commit: str = "a" * 40, *, result_status: str = "PASS") -> dict[str, object]:
    schema = _schema()
    return {
        "schema_version": "0.2.0",
        "claim_id": "R-001",
        "claim_level": "L3_INTERVENTION_SENSITIVE_MECHANISM",
        "claim_text": "A bounded mechanism-level candidate observation.",
        "hypothesis": "The measured state is intervention-sensitive.",
        "competing_hypotheses": ["The observation is explained by a confound."],
        "preregistration_status": "EXPLORATORY",
        "protocol_ref": "docs/protocol.json",
        "protocol_hash": "b" * 64,
        "code_commit": commit,
        "model_or_runtime_ref": "components/example",
        "environment_ref": "qa/environment.json",
        "fixture_refs": ["research-labs/example/fixture.json"],
        "evidence_refs": ["qa/evidence.json"],
        "expected_outcomes": ["intervention changes the measured state"],
        "observed_outcomes": ["measured state changed"],
        "result_status": result_status,
        "deviations": [],
        "limitations": ["synthetic fixture only"],
        "reviewer_status": "SEPARATED_REVIEWED",
        "independent_validation_status": "IVV_NOT_ACHIEVED",
        "canonical_effect": "NONE",
        "provenance": {
            "entities": ["evidence-001"],
            "activities": ["activity-001"],
            "agents": ["reviewer-001"],
            "derived_from": ["fixture-001"],
            "attributed_to": ["reviewer-001"],
            "associated_with": ["activity-001"],
        },
        "evidence_architecture": _architecture(schema),
        "nonclaims": _nonclaims(schema),
    }


def make_root(tmp_path: Path, record: dict[str, object] | None = None) -> tuple[Path, Path]:
    root = tmp_path / "repo"
    for directory in (
        "schemas",
        "docs",
        "components/example",
        "research-labs/example",
        "qa",
    ):
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / "schemas" / "research_evidence_record_v0.2.0.schema.json").write_text(
        json.dumps(_schema()), encoding="utf-8"
    )
    local_files = [
        "docs/protocol.json",
        "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
        "research-labs/example/fixture.json",
        "qa/environment.json",
        "qa/evidence.json",
        "qa/alternative.json",
        "qa/intervention.json",
        "qa/counterfactual.json",
        "qa/provenance.json",
        "qa/admissibility.json",
        "qa/gap.json",
    ]
    for relative in local_files:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    record_path = root / "qa" / "record.json"
    record_path.write_text(json.dumps(record or valid_record()), encoding="utf-8")
    return root, record_path


def test_valid_record_passes_without_mutation(tmp_path: Path) -> None:
    root, path = make_root(tmp_path)
    before = path.read_bytes()
    result = validator.validate_record(root, path, expected_head="a" * 40)
    assert result.status == "PASS"
    assert result.mutation_performed is False
    assert result.canonical_effect == "NONE"
    assert path.read_bytes() == before


def test_missing_local_reference_fails_closed(tmp_path: Path) -> None:
    record = valid_record()
    record["evidence_refs"] = ["qa/missing.json"]
    root, path = make_root(tmp_path, record)
    result = validator.validate_record(root, path, expected_head="a" * 40)
    assert result.status == "FAIL"
    assert any("qa/missing.json" in item for item in result.diagnostics)


def test_local_reference_symlink_outside_root_fails_closed(tmp_path: Path) -> None:
    record = valid_record()
    record["evidence_refs"] = ["qa/external.json"]
    root, path = make_root(tmp_path, record)
    outside = tmp_path / "external.json"
    outside.write_text("{}\n", encoding="utf-8")
    (root / "qa" / "external.json").symlink_to(outside)

    result = validator.validate_record(root, path, expected_head="a" * 40)

    assert result.status == "FAIL"
    assert any("qa/external.json" in item for item in result.diagnostics)


def test_completed_record_must_bind_to_inspected_head(tmp_path: Path) -> None:
    root, path = make_root(tmp_path, valid_record("a" * 40))
    result = validator.validate_record(root, path, expected_head="c" * 40)
    assert result.status == "FAIL"
    assert any("not bound to the inspected head" in item for item in result.diagnostics)


def test_hold_record_may_remain_explicitly_unbound(tmp_path: Path) -> None:
    root, path = make_root(tmp_path, valid_record("a" * 40, result_status="HOLD"))
    result = validator.validate_record(root, path, expected_head="c" * 40)
    assert result.status == "PASS"


def test_open_nonclaim_boundary_fails_schema_validation(tmp_path: Path) -> None:
    record = valid_record()
    nonclaims = record["nonclaims"]
    assert isinstance(nonclaims, dict)
    nonclaims["subjectivity_conclusion"] = "ESTABLISHED"
    root, path = make_root(tmp_path, record)
    result = validator.validate_record(root, path, expected_head="a" * 40)
    assert result.status == "FAIL"
    assert any("schema validation" in item for item in result.diagnostics)


def test_missing_record_returns_hold(tmp_path: Path) -> None:
    root, _ = make_root(tmp_path)
    missing = root / "qa" / "missing-record.json"
    result = validator.validate_record(root, missing, expected_head="a" * 40)
    assert result.status == "HOLD"
