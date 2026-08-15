from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_csomi_slsh_integration.authority import load_default_authorities
from aion_csomi_slsh_integration.contract import build_integration_contract
from aion_csomi_slsh_integration.validate import IntegrationValidationError, validate_record

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "aion_csomi_slsh_integration_v0.1.0.schema.json"
RECORD_PATH = (
    ROOT
    / "research-workbench"
    / "csomi-slsh-integration-2026-08-14"
    / "CSOMI_SLSH_INTEGRATION_RECORD_V0.1.0.json"
)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_record() -> dict:
    return json.loads(RECORD_PATH.read_text(encoding="utf-8"))


def test_exact_frozen_authorities_are_read_only():
    authorities = load_default_authorities(ROOT)
    by_framework = {authority.spec.framework: authority for authority in authorities}
    assert by_framework["CSOMI"].spec.authority_sha == "87405c1877c6f016c303971da13923a1ab690aae"
    assert by_framework["SLSH"].spec.authority_sha == "893d8dc0c1c9d8f9a4188860520143c8d1d3977b"
    assert all(authority.resolved_ref for authority in authorities)


def test_record_is_schema_valid_and_deterministic():
    record = load_record()
    errors = list(Draft202012Validator(load_schema()).iter_errors(record))
    assert not errors
    generated = build_integration_contract(ROOT, load_default_authorities(ROOT))
    assert record == generated


def test_unknown_record_field_fails_closed():
    mutated = deepcopy(load_record())
    mutated["unknown_field"] = "must fail"
    assert list(Draft202012Validator(load_schema()).iter_errors(mutated))


def test_legacy_actor_order_fails_closed():
    mutated = deepcopy(load_record())
    mutated["provenance_contract"]["actor_order"] = ["CODEX_RESEARCH_SYNTHESIS"]
    errors = list(Draft202012Validator(load_schema()).iter_errors(mutated))
    assert errors


def test_unknown_nested_authority_field_fails_closed():
    mutated = deepcopy(load_record())
    mutated["authority_inputs"][0]["unknown_field"] = "must fail"
    assert list(Draft202012Validator(load_schema()).iter_errors(mutated))


@pytest.mark.parametrize(
    "mutation",
    [
        lambda record: record["authority_inputs"][0].update({"authority_sha": "0" * 40}),
        lambda record: record["claim_boundary_rules"].__setitem__(
            1, "CSOMI_EVIDENCE_CONVERGENCE=SUBJECTIVITY_PROOF"
        ),
        lambda record: record.update({"subjectivity_conclusion": "ESTABLISHED"}),
        lambda record: record.update({"experiment_executed": True}),
        lambda record: record["provenance_contract"].update({"provenance_mutation": "ALLOWED"}),
    ],
)
def test_authority_or_boundary_mutation_fails_closed(mutation):
    mutated = deepcopy(load_record())
    mutation(mutated)
    with pytest.raises(IntegrationValidationError):
        validate_record(ROOT, mutated)


def test_adapter_inventories_preserve_namespaces_and_lineage():
    record = load_record()
    inventories = {item["framework"]: item for item in record["adapter_inventories"]}
    assert set(inventories) == {"CSOMI", "SLSH"}
    assert inventories["CSOMI"]["authority_sha"] == "87405c1877c6f016c303971da13923a1ab690aae"
    assert inventories["SLSH"]["authority_sha"] == "893d8dc0c1c9d8f9a4188860520143c8d1d3977b"
    assert inventories["CSOMI"]["claim_ids"] == [
        "CLM-001",
        "CLM-002",
        "CLM-003",
        "CLM-004",
        "CLM-005",
        "CLM-006",
    ]
    assert inventories["SLSH"]["claim_ids"] == [
        "CLM-SLSH-001",
        "CLM-SLSH-002",
        "CLM-SLSH-003",
        "CLM-SLSH-004",
        "CLM-SLSH-005",
    ]
    assert inventories["CSOMI"]["auxiliary_artifacts"][0]["role"] == "CONTROL_IDENTIFIER_ONLY"
    assert inventories["SLSH"]["auxiliary_artifacts"] == []
    assert all(
        item["semantic_projection"] == "IDENTIFIERS_AND_LINEAGE_ONLY"
        for item in inventories.values()
    )
    assert all(
        item["no_source_claim_projection"] is True and item["read_only"] is True
        for item in inventories.values()
    )


def test_per_framework_research_origins_and_source_audit_workflow_are_separate():
    record = load_record()
    provenance = record["provenance_contract"]
    assert provenance["framework_research_origins"]["CSOMI"] == {
        "origin_sequence": ["HUMAN_OWNER_DIRECTION", "CHATGPT_ARCHITECTURE_REFINEMENT"],
        "sequence_semantics": "CSOMI_RESEARCH_ORIGIN_AND_ARCHITECTURE_LINEAGE",
        "not_source_audit_workflow": True,
    }
    assert provenance["framework_research_origins"]["SLSH"] == {
        "origin_sequence": [
            "HUMAN_OWNER_ORIGIN",
            "CHATGPT_ARCHITECTURE_REFINEMENT",
            "CODEX_RESEARCH_SYNTHESIS",
            "EXTERNAL_SOURCE",
        ],
        "sequence_semantics": "SLSH_RESEARCH_ORIGIN_AND_RESEARCH_INPUT_LINEAGE",
        "not_source_audit_workflow": True,
    }
    workflow = provenance["source_audit_materialization_workflow"]
    assert workflow["workflow_name"] == "SOURCE_AUDIT_MATERIALIZATION_WORKFLOW"
    assert workflow["applicability_scope"] == "SLSH_SOURCE_RECORDS_ONLY"
    assert workflow["not_research_origin"] is True
    assert "actor_order" not in provenance
    assert provenance["provenance_mutation"] == "PROHIBITED"


def test_missing_source_audit_scope_fails_closed():
    mutated = deepcopy(load_record())
    del mutated["provenance_contract"]["source_audit_materialization_workflow"][
        "applicability_scope"
    ]
    assert list(Draft202012Validator(load_schema()).iter_errors(mutated))


def test_wrong_source_audit_scope_fails_closed():
    mutated = deepcopy(load_record())
    mutated["provenance_contract"]["source_audit_materialization_workflow"][
        "applicability_scope"
    ] = "CSOMI_AND_SLSH_SOURCE_RECORDS"
    assert list(Draft202012Validator(load_schema()).iter_errors(mutated))


def test_provenance_and_nonmergeable_semantics_are_explicit():
    record = load_record()
    assert record["provenance_contract"]["provenance_mutation"] == "PROHIBITED"
    assert "CSOMI.subjectivity_conclusion" in record["known_nonmergeable_fields"]
    assert "SLSH.functional_rule" in record["known_nonmergeable_fields"]
    assert all(
        item["status"] == "PRESERVED_NOT_RECONCILED"
        for item in record["unresolved_metadata_conditions"]
    )
    assert all(
        item["resolution_policy"] == "HOLD_FOR_OWNER_OR_FRAMEWORK_AUTHORITY"
        for item in record["unresolved_metadata_conditions"]
    )


def test_no_execution_or_canonical_writeback_state():
    record = load_record()
    assert record["canonical_effect"] == "NONE"
    assert record["deployment"] is False
    assert record["experiment_executed"] is False
    assert record["runtime_executed"] is False
    assert record["model_modified"] is False
    assert record["live_data_collected"] is False
    assert record["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert (
        record["control_falsifier_contract"]["cross_framework_execution"]
        == "NO_EXPERIMENT_NO_RUNTIME_NO_LIVE_DATA"
    )
