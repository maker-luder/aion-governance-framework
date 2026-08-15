from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .authority import (
    CSOMI_SPEC,
    ReadOnlyAuthority,
    assert_authority_semantics,
    load_default_authorities,
)
from .contract import build_integration_contract


class IntegrationValidationError(AssertionError):
    """Raised when an integration contract is not safe to admit."""


def _validate_json(schema: dict[str, Any], value: dict[str, Any], label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value), key=lambda error: list(error.path)
    )
    if errors:
        first = errors[0]
        location = ".".join(str(item) for item in first.path) or "$"
        raise IntegrationValidationError(f"{label} invalid at {location}: {first.message}")


def validate_authority_inputs(
    root: Path, authorities: tuple[ReadOnlyAuthority, ReadOnlyAuthority]
) -> None:
    by_framework = {authority.spec.framework: authority for authority in authorities}
    if set(by_framework) != {"CSOMI", "SLSH"}:
        raise IntegrationValidationError("exactly CSOMI and SLSH authority inputs are required")
    for authority in authorities:
        assert_authority_semantics(authority)
        _validate_json(
            authority.schema, authority.packet, f"{authority.spec.framework} frozen packet"
        )
        if authority.resolved_ref not in {
            authority.spec.authority_sha,
            authority.spec.authority_ref,
            f"refs/remotes/origin/{authority.spec.authority_ref}",
            f"refs/heads/{authority.spec.authority_ref}",
        }:
            raise IntegrationValidationError(
                f"unexpected resolved ref for {authority.spec.framework}"
            )

    csomi = by_framework["CSOMI"]
    slsh = by_framework["SLSH"]
    if slsh.packet.get("base_head") != CSOMI_SPEC.authority_sha:
        raise IntegrationValidationError(
            "SLSH packet base_head changed away from CSOMI authority SHA"
        )
    if slsh.packet["csomi_interface"]["accepted_csomi_source_sha"] != CSOMI_SPEC.authority_sha:
        raise IntegrationValidationError("SLSH conditional interface pins a different CSOMI SHA")
    if csomi.packet["branch"] != "research/cross-substrate-other-minds-inference-20260814":
        raise IntegrationValidationError("CSOMI packet branch drift")
    if slsh.packet["branch"] != "research/subjective-load-sensitivity-hypothesis-20260814":
        raise IntegrationValidationError("SLSH packet branch drift")


def validate_record(
    root: Path, record: dict[str, Any]
) -> tuple[ReadOnlyAuthority, ReadOnlyAuthority]:
    schema_path = root / "schemas" / "aion_csomi_slsh_integration_v0.1.0.schema.json"
    schema = __import__("json").loads(schema_path.read_text(encoding="utf-8"))
    _validate_json(schema, record, "integration record")
    authorities = load_default_authorities(root)
    validate_authority_inputs(root, authorities)
    by_framework = {authority.spec.framework: authority for authority in authorities}
    expected_record = build_integration_contract(root, authorities)
    if record != expected_record:
        raise IntegrationValidationError(
            "integration record differs from deterministic materialization"
        )
    for item in record["authority_inputs"]:
        authority = by_framework[item["framework"]]
        if item["authority_sha"] != authority.spec.authority_sha:
            raise IntegrationValidationError(f"{item['framework']} record SHA mismatch")
        if (
            item["packet_sha256"] != authority.packet_sha256
            or item["schema_sha256"] != authority.schema_sha256
        ):
            raise IntegrationValidationError(f"{item['framework']} record content hash mismatch")
        if item["read_only"] is not True or item["mutation_policy"] != "MUTATION_PROHIBITED":
            raise IntegrationValidationError(f"{item['framework']} adapter is not read-only")
    provenance = record["provenance_contract"]
    expected_origins = {
        "CSOMI": ["HUMAN_OWNER_DIRECTION", "CHATGPT_ARCHITECTURE_REFINEMENT"],
        "SLSH": [
            "HUMAN_OWNER_ORIGIN",
            "CHATGPT_ARCHITECTURE_REFINEMENT",
            "CODEX_RESEARCH_SYNTHESIS",
            "EXTERNAL_SOURCE",
        ],
    }
    for framework, sequence in expected_origins.items():
        origin = provenance["framework_research_origins"][framework]
        if origin["origin_sequence"] != sequence or origin["not_source_audit_workflow"] is not True:
            raise IntegrationValidationError(f"{framework} research-origin provenance drift")
    workflow = provenance["source_audit_materialization_workflow"]
    if workflow["workflow_name"] != "SOURCE_AUDIT_MATERIALIZATION_WORKFLOW":
        raise IntegrationValidationError("source-audit workflow name drift")
    if workflow["applicability_scope"] != "SLSH_SOURCE_RECORDS_ONLY":
        raise IntegrationValidationError("source-audit workflow applicability scope drift")
    if workflow["not_research_origin"] is not True:
        raise IntegrationValidationError(
            "source-audit workflow is not separated from research-origin provenance"
        )
    if "actor_order" in provenance:
        raise IntegrationValidationError("legacy single actor_order provenance must not be present")
    if record["claim_boundary_rules"] != [
        "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION",
        "CSOMI_EVIDENCE_CONVERGENCE != SUBJECTIVITY_PROOF",
        "SLSH_FUNCTIONAL_LOAD != SUBJECTIVE_LOAD",
    ]:
        raise IntegrationValidationError("claim-boundary rules drift")
    if record["canonical_effect"] != "NONE" or record["deployment"] is not False:
        raise IntegrationValidationError("canonical/deployment boundary drift")
    if any(
        record[field] is not False
        for field in (
            "experiment_executed",
            "runtime_executed",
            "model_modified",
            "live_data_collected",
        )
    ):
        raise IntegrationValidationError("execution boundary drift")
    if record["subjectivity_conclusion"] != "NOT_ESTABLISHED":
        raise IntegrationValidationError("subjectivity conclusion boundary drift")
    return authorities


def validate_file(root: Path) -> None:
    import json

    record_path = (
        root
        / "research-workbench"
        / "csomi-slsh-integration-2026-08-14"
        / "CSOMI_SLSH_INTEGRATION_RECORD_V0.1.0.json"
    )
    record = json.loads(record_path.read_text(encoding="utf-8"))
    validate_record(root, record)
    print(
        "CSOMI×SLSH integration validation PASS: exact authorities, schema, lineage, "
        "boundaries, provenance and no-execution contract"
    )
