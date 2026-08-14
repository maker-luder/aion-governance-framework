from __future__ import annotations

from pathlib import Path
from typing import Any

from .authority import ReadOnlyAuthority
from .adapters import build_adapter_inventory


COMMON_SHARED_FIELDS = [
    "framework_and_exact_sha",
    "packet_id",
    "claim_id_or_type",
    "status",
    "disposition",
    "evidence_role",
    "allowed_update",
    "forbidden_update",
]

CLAIM_PRESERVED_FIELDS = [
    "framework",
    "claim_id",
    "claim_type",
    "claim_text",
    "status",
    "disposition",
    "subjectivity_conclusion",
]

EVIDENCE_PRESERVED_FIELDS = [
    "framework",
    "evidence_id",
    "claim_id",
    "channel_ids",
    "support_direction",
    "alternative_explanations",
    "cross_substrate_transfer",
    "update",
    "status",
]

CONTROL_PRESERVED_FIELDS = ["framework", "control_id", "control_type", "name", "purpose"]
FALSIFIER_PRESERVED_FIELDS = [
    "framework",
    "falsifier_id",
    "condition",
    "effect_or_weakens",
    "status_or_machine_effect",
]
LINEAGE_PRESERVED_FIELDS = [
    "framework",
    "authority_ref",
    "authority_sha",
    "packet_path",
    "schema_path",
    "packet_sha256",
    "schema_sha256",
    "read_only",
    "mutation_policy",
]


def _claim_projection(authorities: tuple[ReadOnlyAuthority, ReadOnlyAuthority]) -> dict[str, Any]:
    return {
        "shared_fields": COMMON_SHARED_FIELDS,
        "preserved_fields": CLAIM_PRESERVED_FIELDS,
        "non_equivalence_guard": "CSOMI_CLAIM_TYPE_AND_SLSH_CLAIM_TYPE_ARE_NOT_SEMANTICALLY_COERCED",
        "adapter_output_only": True,
    }


def _evidence_projection() -> dict[str, Any]:
    return {
        "shared_fields": COMMON_SHARED_FIELDS,
        "preserved_fields": EVIDENCE_PRESERVED_FIELDS,
        "non_equivalence_guard": "CSOMI_EVIDENCE_CONVERGENCE!=SUBJECTIVITY_PROOF",
        "adapter_output_only": True,
    }


def _control_projection() -> dict[str, Any]:
    return {
        "shared_fields": ["framework", "control_id", "control_type", "name", "purpose", "diagnostic_role"],
        "preserved_fields": CONTROL_PRESERVED_FIELDS,
        "non_equivalence_guard": "CONTROLS_ARE_DIAGNOSTIC_NOT_SUBJECTIVITY_PROOF",
        "adapter_output_only": True,
    }


def _falsifier_projection() -> dict[str, Any]:
    return {
        "shared_fields": ["framework", "falsifier_id", "condition", "effect", "status"],
        "preserved_fields": FALSIFIER_PRESERVED_FIELDS,
        "non_equivalence_guard": "FALSIFIER_TRIGGER_DOWNDATES_OR_HOLDS_LOCAL_SCOPE_ONLY",
        "adapter_output_only": True,
    }


def _lineage_projection(authorities: tuple[ReadOnlyAuthority, ReadOnlyAuthority]) -> dict[str, Any]:
    return {
        "shared_fields": ["framework", "authority_ref", "authority_sha", "packet_path", "schema_path"],
        "preserved_fields": LINEAGE_PRESERVED_FIELDS,
        "non_equivalence_guard": "EXACT_SHA_AND_FRAMEWORK_IDENTITY_REQUIRED_FOR_EVERY_ADAPTER_RECORD",
        "adapter_output_only": True,
    }


def build_integration_contract(
    root: Path,
    authorities: tuple[ReadOnlyAuthority, ReadOnlyAuthority],
) -> dict[str, Any]:
    frameworks = {authority.spec.framework for authority in authorities}
    if frameworks != {"CSOMI", "SLSH"}:
        raise ValueError("integration requires exactly one CSOMI and one SLSH authority")
    for authority in authorities:
        if not authority.spec.authority_sha or not authority.packet_sha256 or not authority.schema_sha256:
            raise ValueError("authority lineage is incomplete")

    return {
        "schema_version": "0.1.0",
        "record_id": "AION_CSOMI_SLSH_INTEGRATION_RECORD_V0.1.0",
        "integration_id": "CSOMI_SLSH_READ_ONLY_INTERFACE_RECONCILIATION_V0.1.0",
        "integration_branch": "integration/csomi-slsh-semantic-reconciliation-20260814",
        "integration_scope": "READ_ONLY_INTERFACE_BOUNDARY_PROVENANCE_AND_CONSISTENCY_ONLY",
        "authority_inputs": [
            {
                "framework": authority.spec.framework,
                "authority_ref": authority.spec.authority_ref,
                "authority_sha": authority.spec.authority_sha,
                "packet_path": authority.spec.packet_path,
                "schema_path": authority.spec.schema_path,
                "packet_sha256": authority.packet_sha256,
                "schema_sha256": authority.schema_sha256,
                "declared_packet_branch": authority.packet.get("branch", authority.spec.authority_ref),
                "read_only": True,
                "mutation_policy": "MUTATION_PROHIBITED",
                "adapter_mode": "READ_ONLY_GIT_OBJECT_ADAPTER",
                "source_semantics_not_copied": True,
            }
            for authority in sorted(authorities, key=lambda item: item.spec.framework)
        ],
        "adapter_inventories": [
            build_adapter_inventory(root=root, authority=authority)
            for authority in sorted(authorities, key=lambda item: item.spec.framework)
        ],
        "shared_interface": {
            "authority_identity": "FRAMEWORK_AND_EXACT_SHA_REQUIRED; NO_SEMANTIC_MERGE",
            "claim_projection": _claim_projection(authorities),
            "evidence_projection": _evidence_projection(),
            "control_projection": _control_projection(),
            "falsifier_projection": _falsifier_projection(),
            "lineage_projection": _lineage_projection(authorities),
        },
        "claim_boundary_rules": [
            "RESEARCH_TOPIC != CAPABILITY != SCIENTIFIC_CONCLUSION",
            "CSOMI_EVIDENCE_CONVERGENCE != SUBJECTIVITY_PROOF",
            "SLSH_FUNCTIONAL_LOAD != SUBJECTIVE_LOAD",
        ],
        "provenance_contract": {
            "actor_order": [
                "CODEX_RESEARCH_SYNTHESIS",
                "CHATGPT_INDEPENDENT_SOURCE_REVIEW",
                "HUMAN_OWNER_APPROVAL_OR_GOVERNANCE_DECISION",
                "MANUS_IMPLEMENTATION",
            ],
            "authority_attribution": "FROZEN_INPUTS_REMAIN_AUTHORITATIVE_FOR_OWN_SEMANTICS",
            "source_attribution": "NO_SOURCE_RECORDS_COPIED_OR_RECLASSIFIED",
            "implementation_attribution": "MANUS_IMPLEMENTATION_ONLY_NOT_SCIENTIFIC_REVIEW",
            "provenance_mutation": "PROHIBITED",
        },
        "evidence_role_contract": {
            "csomi_roles": [
                "BOUNDED_CAPABILITY",
                "GRADED_HYPOTHESIS_CREDENCE",
                "MECHANISTIC_OR_CAUSAL_SUPPORT",
                "THEORY_CONDITIONAL_SUPPORT",
                "DISANALOGY_DISCOUNT",
                "ALTERNATIVE_COMPARISON",
                "ROBUSTNESS_STATUS",
            ],
            "slsh_roles": [
                "FUNCTIONAL_LOAD_STATE",
                "NON_AFFECTIVE_ALTERNATIVE",
                "CAUSAL_SIGNATURE",
                "CONTROL_DIAGNOSTIC",
                "FALSIFIER",
                "CLAIM_BOUNDARY",
            ],
            "convergence_boundary": "CSOMI_EVIDENCE_CONVERGENCE!=SUBJECTIVITY_PROOF",
            "subjectivity_proof": "PROHIBITED",
        },
        "control_falsifier_contract": {
            "namespacing": "FRAMEWORK_FIELD_REQUIRED_RAW_AUTHORITY_IDS_PRESERVED_NO_ID_COERCION",
            "control_semantics": "CONTROLS_ARE_DIAGNOSTIC_NOT_SUBJECTIVITY_PROOF",
            "falsifier_semantics": "FALSIFIERS_DOWNDATE_OR_HOLD_LOCAL_SCOPE_ONLY",
            "cross_framework_execution": "NO_EXPERIMENT_NO_RUNTIME_NO_LIVE_DATA",
        },
        "known_nonmergeable_fields": [
            "CSOMI.subjectivity_conclusion",
            "CSOMI.consciousness_conclusion",
            "CSOMI.identity_continuity_conclusion",
            "SLSH.subjective_load_sensitivity",
            "SLSH.subjectivity_conclusion",
            "SLSH.functional_rule",
            "framework_specific_claim_type",
            "framework_specific_evidence_status",
        ],
        "unresolved_metadata_conditions": [
            {
                "id": "META-001",
                "status": "PRESERVED_NOT_RECONCILED",
                "field": "CSOMI.packet_path_vs_SLSH.csomi_interface",
                "detail": "SLSH retains a conditional read-only CSOMI interface; this module records the exact input hashes without copying or implementing that interface.",
                "resolution_policy": "HOLD_FOR_OWNER_OR_FRAMEWORK_AUTHORITY",
            },
            {
                "id": "META-002",
                "status": "PRESERVED_NOT_RECONCILED",
                "field": "framework_specific_claim_semantics",
                "detail": "CSOMI mind-like inference claims and SLSH load-state claims remain distinct namespaces and are not joined into a scientific conclusion.",
                "resolution_policy": "HOLD_FOR_OWNER_OR_FRAMEWORK_AUTHORITY",
            },
        ],
        "canonical_effect": "NONE",
        "deployment": False,
        "experiment_executed": False,
        "runtime_executed": False,
        "model_modified": False,
        "live_data_collected": False,
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "admission_status": "INTEGRATION_MODULE_COMPLETE_PENDING_CHATGPT_OWNER_REVIEW",
    }
