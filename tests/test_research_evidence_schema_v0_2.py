from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "schemas" / "research_evidence_record.schema.json"
V2 = ROOT / "schemas" / "research_evidence_record_v0.2.0.schema.json"


def _validator(path: Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _v2_record() -> dict[str, object]:
    return {
        "schema_version": "0.2.0",
        "claim_id": "RESEARCH-CLAIM-001",
        "claim_level": "L3_INTERVENTION_SENSITIVE_MECHANISM",
        "claim_text": "A bounded subjectivity-relevant mechanism candidate.",
        "hypothesis": "The measured state is intervention-sensitive under the standing method.",
        "competing_hypotheses": ["The effect is explained by retrieval context alone."],
        "preregistration_status": "EXPLORATORY",
        "protocol_ref": "research-protocol-001",
        "protocol_hash": "a" * 64,
        "code_commit": "b" * 40,
        "model_or_runtime_ref": "research-runtime-candidate",
        "environment_ref": "env-evidence-001",
        "fixture_refs": ["fixture-001"],
        "evidence_refs": ["evidence-001"],
        "expected_outcomes": ["intervention changes the measured state"],
        "observed_outcomes": ["measured state changed"],
        "result_status": "CONTRADICTORY",
        "deviations": [],
        "limitations": ["single bounded fixture"],
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
        "evidence_architecture": {
            "standing_inference_stage_ref": "whitepaper:v0.14.21:four-stage:mechanism",
            "dimension_ref": "whitepaper:v0.14.21:AB.6:causal-boundary",
            "alternative_explanation_refs": ["alternative-001"],
            "causal_intervention_refs": ["intervention-001"],
            "ablation_refs": [],
            "counterfactual_refs": ["counterfactual-001"],
            "robustness_refs": [],
            "replication_refs": [],
            "provenance_refs": ["evidence-001"],
            "admissibility_ref": "admissibility-review-001",
            "claim_scope": "subjectivity-relevant mechanism candidate only",
            "unresolved_gap_refs": ["gap-001"],
            "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
            "inference_stage": "MECHANISM",
            "alternative_explanations": ["retrieval-context confound"],
        },
        "nonclaims": {
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "moral_status_conclusion": "NOT_ESTABLISHED",
            "legal_status_conclusion": "OUT_OF_SCOPE",
            "main_effect": "NONE",
            "canonical_effect": "NONE",
            "live_runtime_effect": "NONE",
            "runtime_effect": "NONE",
        },
    }


def _legacy_v1_record() -> dict[str, object]:
    record = _v2_record()
    record.pop("schema_version")
    record.pop("evidence_architecture")
    record.pop("nonclaims")
    record["result_status"] = "HOLD"
    return record


def test_v2_candidate_accepts_exact_standing_ab6_reference() -> None:
    assert list(_validator(V2).iter_errors(_v2_record())) == []


def test_v2_candidate_rejects_invented_dimension_reference() -> None:
    record = _v2_record()
    architecture = record["evidence_architecture"]
    assert isinstance(architecture, dict)
    architecture["dimension_ref"] = "whitepaper:v0.14.21:AB.6:subjectivity-score"
    assert list(_validator(V2).iter_errors(record))


def test_v2_candidate_rejects_score_or_authority_fields() -> None:
    record = _v2_record()
    architecture = record["evidence_architecture"]
    assert isinstance(architecture, dict)
    architecture["subjectivity_score"] = 0.9
    assert list(_validator(V2).iter_errors(record))


def test_v2_candidate_rejects_non_digest_protocol_hash() -> None:
    record = _v2_record()
    record["protocol_hash"] = "not-a-digest"
    assert list(_validator(V2).iter_errors(record))


def test_v2_candidate_rejects_subjectivity_promotion() -> None:
    record = _v2_record()
    nonclaims = record["nonclaims"]
    assert isinstance(nonclaims, dict)
    nonclaims["subjectivity_conclusion"] = "ESTABLISHED"
    assert list(_validator(V2).iter_errors(record))


def test_v1_historical_schema_remains_valid_for_legacy_shape() -> None:
    assert list(_validator(V1).iter_errors(_legacy_v1_record())) == []


def test_duplicate_dimension_support_refs_fail_closed() -> None:
    record = copy.deepcopy(_v2_record())
    architecture = record["evidence_architecture"]
    assert isinstance(architecture, dict)
    architecture["provenance_refs"] = ["evidence-001", "evidence-001"]
    assert list(_validator(V2).iter_errors(record))


def test_duplicate_evidence_refs_fail_closed() -> None:
    record = copy.deepcopy(_v2_record())
    record["evidence_refs"] = ["evidence-001", "evidence-001"]
    assert list(_validator(V2).iter_errors(record))
