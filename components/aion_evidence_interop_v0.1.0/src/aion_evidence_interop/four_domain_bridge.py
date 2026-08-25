from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

from .canonical import InteropError, canonical_json_bytes

FOUR_DOMAIN_SOURCE_REPOSITORY = "maker-luder/aion-governance-framework"
FOUR_DOMAIN_SOURCE_BRANCH = "review/four-domain-research-materialization"
FOUR_DOMAIN_SOURCE_HEAD = "f654b5032ebc45058a64e81d409149ee7ea4bfbe"
FOUR_DOMAIN_SOURCE_STATE = "INDEFINITE_FROZEN_CHECKPOINT"
FOUR_DOMAIN_SOURCE_ARTIFACT = (
    "research-workbench/four-domain-materialization/2026-08-09/"
    "FOUR_DOMAIN_REPOSITORY_CROSSWALK.md"
)
FOUR_DOMAIN_SOURCE_BLOB_SHA1 = "7e55741b85b27d383b4b721b834b1744c6c03fb9"

BRIDGE_SCHEMA_VERSION = "0.1.0"
BRIDGE_PROTOCOL_REF = (
    "components/aion_evidence_interop_v0.1.0/docs/FOUR_DOMAIN_BRIDGE.md"
)
BRIDGE_DESCRIPTOR_REF = (
    "components/aion_evidence_interop_v0.1.0/"
    "fixtures/four_domain_snapshot_descriptor.json"
)
BRIDGE_ENVIRONMENT_REF = "components/aion_evidence_interop_v0.1.0/README.md"

EXPECTED_DESCRIPTOR_KEYS = {
    "schema_version",
    "source_repository",
    "source_branch",
    "source_head",
    "source_state",
    "source_artifact",
    "claim_id",
    "construct",
    "implementation_status",
    "claim_text",
    "hypothesis",
    "competing_hypotheses",
    "observation",
    "mechanism",
    "interpretation",
    "limitations",
    "alternative_explanations",
    "unresolved_gaps",
}

ALLOWED_IMPLEMENTATION_STATUSES = {
    "MIXED_BOUNDED_STATUS",
    "REUSABLE_EXISTING_SERVICE",
    "REUSABLE_WITH_ADAPTER",
    "ALREADY_IMPLEMENTED",
    "PARTIAL_OVERLAP",
    "DESIGN_GAP",
    "RESEARCH_DEFINITION_REQUIRED",
}


def _require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InteropError(
            f"Four-Domain bridge descriptor requires non-empty {field}",
            category="bridge_descriptor_failure",
        )
    return value


def _require_string_list(value: Any, field: str, *, min_items: int = 0) -> list[str]:
    if not isinstance(value, list) or len(value) < min_items:
        raise InteropError(
            f"Four-Domain bridge descriptor requires {field} list",
            category="bridge_descriptor_failure",
        )
    result: list[str] = []
    for item in value:
        text = _require_nonempty_string(item, field)
        if text in result:
            raise InteropError(
                f"Four-Domain bridge descriptor {field} contains duplicates",
                category="bridge_descriptor_failure",
            )
        result.append(text)
    return result


def _validate_source_path(value: str) -> None:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        raise InteropError(
            "Four-Domain source artifact must be a normalized repository-relative path",
            category="bridge_descriptor_failure",
        )


def validate_four_domain_descriptor(descriptor: dict[str, Any]) -> None:
    if set(descriptor) != EXPECTED_DESCRIPTOR_KEYS:
        missing = sorted(EXPECTED_DESCRIPTOR_KEYS - set(descriptor))
        extra = sorted(set(descriptor) - EXPECTED_DESCRIPTOR_KEYS)
        raise InteropError(
            f"Four-Domain bridge descriptor keys mismatch: missing={missing} extra={extra}",
            category="bridge_descriptor_failure",
        )

    expected_constants = {
        "schema_version": BRIDGE_SCHEMA_VERSION,
        "source_repository": FOUR_DOMAIN_SOURCE_REPOSITORY,
        "source_branch": FOUR_DOMAIN_SOURCE_BRANCH,
        "source_head": FOUR_DOMAIN_SOURCE_HEAD,
        "source_state": FOUR_DOMAIN_SOURCE_STATE,
    }
    for field, expected in expected_constants.items():
        if descriptor.get(field) != expected:
            raise InteropError(
                f"Four-Domain bridge descriptor is not pinned to {field}={expected}",
                category="bridge_descriptor_failure",
            )

    source_artifact = descriptor.get("source_artifact")
    if not isinstance(source_artifact, dict) or set(source_artifact) != {
        "path",
        "git_blob_sha1",
    }:
        raise InteropError(
            "Four-Domain bridge source_artifact must contain only path and git_blob_sha1",
            category="bridge_descriptor_failure",
        )
    source_path = _require_nonempty_string(source_artifact.get("path"), "source_artifact.path")
    _validate_source_path(source_path)
    if source_path != FOUR_DOMAIN_SOURCE_ARTIFACT:
        raise InteropError(
            "Four-Domain bridge descriptor source artifact path is not the pinned crosswalk",
            category="bridge_descriptor_failure",
        )
    blob_sha = _require_nonempty_string(
        source_artifact.get("git_blob_sha1"), "source_artifact.git_blob_sha1"
    )
    if re.fullmatch(r"[0-9a-f]{40}", blob_sha) is None:
        raise InteropError(
            "Four-Domain source Git blob SHA-1 must be lowercase 40-hex",
            category="bridge_descriptor_failure",
        )
    if blob_sha != FOUR_DOMAIN_SOURCE_BLOB_SHA1:
        raise InteropError(
            "Four-Domain bridge descriptor source Git blob SHA-1 does not match the pinned crosswalk",
            category="bridge_descriptor_failure",
        )

    for field in (
        "claim_id",
        "construct",
        "claim_text",
        "hypothesis",
        "observation",
        "mechanism",
        "interpretation",
    ):
        _require_nonempty_string(descriptor.get(field), field)

    status = _require_nonempty_string(
        descriptor.get("implementation_status"), "implementation_status"
    )
    if status not in ALLOWED_IMPLEMENTATION_STATUSES:
        raise InteropError(
            f"unsupported Four-Domain implementation status: {status}",
            category="bridge_descriptor_failure",
        )

    _require_string_list(
        descriptor.get("competing_hypotheses"), "competing_hypotheses", min_items=1
    )
    _require_string_list(descriptor.get("limitations"), "limitations", min_items=1)
    _require_string_list(
        descriptor.get("alternative_explanations"),
        "alternative_explanations",
        min_items=1,
    )
    _require_string_list(descriptor.get("unresolved_gaps"), "unresolved_gaps")


def exact_source_url() -> str:
    return (
        f"https://github.com/{FOUR_DOMAIN_SOURCE_REPOSITORY}/blob/"
        f"{FOUR_DOMAIN_SOURCE_HEAD}/{quote(FOUR_DOMAIN_SOURCE_ARTIFACT, safe='/')}"
    )


def _gap_ref(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return f"urn:aion:four-domain:unresolved:{digest}"


def bridge_protocol_hash(root: Path) -> str:
    root = root.resolve()
    protocol = (root / BRIDGE_PROTOCOL_REF).resolve(strict=True)
    try:
        protocol.relative_to(root)
    except ValueError as exc:
        raise InteropError(
            "Four-Domain bridge protocol escapes repository root",
            category="path_confinement_failure",
        ) from exc
    if not protocol.is_file():
        raise InteropError("Four-Domain bridge protocol is missing")
    return hashlib.sha256(protocol.read_bytes()).hexdigest()


def materialize_four_domain_record(
    root: Path,
    descriptor: dict[str, Any],
) -> dict[str, Any]:
    validate_four_domain_descriptor(descriptor)
    source_url = exact_source_url()
    limitations = list(descriptor["limitations"])
    fixed_limitation = (
        "This bridge does not fetch, execute, or re-run the frozen Four-Domain research "
        "branch at runtime."
    )
    if fixed_limitation not in limitations:
        limitations.append(fixed_limitation)

    unresolved_gap_refs = [_gap_ref(item) for item in descriptor["unresolved_gaps"]]

    return {
        "schema_version": "0.2.0",
        "claim_id": descriptor["claim_id"],
        "claim_level": "L0_OBSERVATION",
        "claim_text": descriptor["claim_text"],
        "hypothesis": descriptor["hypothesis"],
        "competing_hypotheses": list(descriptor["competing_hypotheses"]),
        "preregistration_status": "EXPLORATORY",
        "protocol_ref": BRIDGE_PROTOCOL_REF,
        "protocol_hash": bridge_protocol_hash(root),
        "code_commit": FOUR_DOMAIN_SOURCE_HEAD,
        "model_or_runtime_ref": "FOUR_DOMAIN_HISTORICAL_WORKBENCH_INSPECTION_ONLY",
        "environment_ref": BRIDGE_ENVIRONMENT_REF,
        "fixture_refs": [BRIDGE_DESCRIPTOR_REF],
        "evidence_refs": [source_url],
        "expected_outcomes": [
            "Pinned Four-Domain source metadata remains externally traceable without "
            "canonical, deployment, identity, consciousness, or subjectivity promotion."
        ],
        "observed_outcomes": [],
        "result_status": "HOLD",
        "deviations": [],
        "limitations": limitations,
        "reviewer_status": "UNREVIEWED",
        "independent_validation_status": "IVV_NOT_ACHIEVED",
        "canonical_effect": "NONE",
        "provenance": {
            "entities": [
                source_url,
                f"urn:git:blob:sha1:{FOUR_DOMAIN_SOURCE_BLOB_SHA1}",
            ],
            "activities": [
                "FOUR_DOMAIN_REPOSITORY_FACT_EXTRACTION",
                "AION_FOUR_DOMAIN_READ_ONLY_BRIDGE",
            ],
            "agents": [
                "CODEX_SOURCE_CROSSWALK_DECLARED_ATTRIBUTION",
                "CHATGPT_BRIDGE_DESIGN_AND_IMPLEMENTATION",
            ],
            "derived_from": [source_url],
            "attributed_to": [
                "CODEX_SOURCE_CROSSWALK_DECLARED_ATTRIBUTION",
                "CHATGPT_BRIDGE_DESIGN_AND_IMPLEMENTATION",
            ],
            "associated_with": [
                f"{FOUR_DOMAIN_SOURCE_BRANCH}@{FOUR_DOMAIN_SOURCE_HEAD}"
            ],
        },
        "evidence_architecture": {
            "alternative_explanation_refs": [source_url],
            "causal_intervention_refs": [],
            "ablation_refs": [],
            "counterfactual_refs": [],
            "robustness_refs": [],
            "replication_refs": [],
            "provenance_refs": [source_url, BRIDGE_PROTOCOL_REF],
            "admissibility_ref": BRIDGE_PROTOCOL_REF,
            "claim_scope": (
                "Historical Four-Domain repository mapping materialization only; no "
                "research execution, scientific promotion, canonical effect, or deployment."
            ),
            "unresolved_gap_refs": unresolved_gap_refs,
            "method_ref": "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md",
            "inference_stage": "OBSERVATION",
            "observation": descriptor["observation"],
            "mechanism": descriptor["mechanism"],
            "interpretation": descriptor["interpretation"],
            "alternative_explanations": list(descriptor["alternative_explanations"]),
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


def materialize_four_domain_record_bytes(
    root: Path,
    descriptor: dict[str, Any],
) -> bytes:
    return canonical_json_bytes(materialize_four_domain_record(root, descriptor))


def load_four_domain_descriptor(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InteropError(
            "Four-Domain bridge descriptor must be readable UTF-8 JSON",
            category="bridge_descriptor_failure",
        ) from exc
    if not isinstance(value, dict):
        raise InteropError(
            "Four-Domain bridge descriptor must be a JSON object",
            category="bridge_descriptor_failure",
        )
    validate_four_domain_descriptor(value)
    return value
