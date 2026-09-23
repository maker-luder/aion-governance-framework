"""Phase B materialization decisions bound to the Phase A v0.2 ledger.

The Phase A matrix remains the provenance and semantic-inventory authority.
This module adds only admission decisions and reuses its repository binding
verifier instead of creating a parallel evidence system.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json
from pathlib import Path
from typing import Any

from .coverage_matrix import (
    CoverageClassification,
    CoverageDisposition,
    EmbodimentArchiveCoverageMatrix,
    SemanticUnitCoverage,
    coverage_matrix_hash,
    validate_coverage_matrix,
    validate_coverage_matrix_bindings,
)


class MaterializationDecision(StrEnum):
    IMPLEMENT_EXISTING_TARGET = "IMPLEMENT_EXISTING_TARGET"
    EXTEND_EXISTING_TARGET = "EXTEND_EXISTING_TARGET"
    KEEP_DEFERRED = "KEEP_DEFERRED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    NEEDS_NEW_TARGET = "NEEDS_NEW_TARGET"


class MaterializationAdmissionStatus(StrEnum):
    ACTIVE_VERIFIED = "ACTIVE_VERIFIED"
    KEPT_DEFERRED = "KEPT_DEFERRED"
    EXCLUDED_SUPERSEDED = "EXCLUDED_SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    NOT_ADMITTED = "NOT_ADMITTED"


class MaterializationArchitectureLayer(StrEnum):
    SHARED_EMBODIMENT_CORE = "SHARED_EMBODIMENT_CORE"
    INDIVIDUAL_EMBODIMENT_PROFILE = "INDIVIDUAL_EMBODIMENT_PROFILE"
    FUNCTIONAL_PHYSIOLOGY = "FUNCTIONAL_PHYSIOLOGY"
    SENSORIMOTOR = "SENSORIMOTOR"
    RUNTIME = "RUNTIME"
    LONGITUDINAL = "LONGITUDINAL"


class MaterializationRoleScope(StrEnum):
    SHARED = "SHARED"
    AION_ASTRA = "AION_ASTRA"
    CHATGPT_TEACHER = "CHATGPT_TEACHER"
    EXTERNAL = "EXTERNAL"


@dataclass(frozen=True, slots=True)
class MaterializationEntry:
    semantic_unit_id: str
    source_pr: int
    source_head: str
    source_path: str
    source_blob_sha: str
    source_locator: str
    phase_a_classification: CoverageClassification
    phase_a_disposition: CoverageDisposition
    decision: MaterializationDecision
    admission_status: MaterializationAdmissionStatus
    architecture_layer: MaterializationArchitectureLayer
    role_scope: MaterializationRoleScope
    target_ref: str
    active_target_ref: str | None
    replacement_ref: str | None
    canonical_owner_unit_id: str | None
    reason: str


@dataclass(frozen=True, slots=True)
class EmbodimentMaterializationMap:
    map_id: str
    phase_a_matrix_id: str
    phase_a_matrix_sha256: str
    entries: tuple[MaterializationEntry, ...]
    canonical_order: tuple[str, ...]
    scientific_disposition: str
    subjectivity: str
    canonical_effect: str
    deployment: bool


_ENTRY_KEYS = {
    "semantic_unit_id",
    "source_pr",
    "source_head",
    "source_path",
    "source_blob_sha",
    "source_locator",
    "phase_a_classification",
    "phase_a_disposition",
    "decision",
    "admission_status",
    "architecture_layer",
    "role_scope",
    "target_ref",
    "active_target_ref",
    "replacement_ref",
    "canonical_owner_unit_id",
    "reason",
}
_MAP_KEYS = {
    "map_id",
    "phase_a_matrix_id",
    "phase_a_matrix_sha256",
    "entries",
    "canonical_order",
    "scientific_disposition",
    "subjectivity",
    "canonical_effect",
    "deployment",
}
CANONICAL_MATERIALIZATION_ORDER = (
    "source_pr",
    "source_path",
    "semantic_unit_id",
)


def _mapping(value: object, keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != keys:
        raise ValueError(f"{label} must contain exact fields")
    return value


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    return value


def _nullable_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _load_entry(value: object) -> MaterializationEntry:
    raw = _mapping(value, _ENTRY_KEYS, "materialization entry")
    source_pr = raw["source_pr"]
    if type(source_pr) is not int:
        raise ValueError("source_pr must be an exact integer")
    return MaterializationEntry(
        semantic_unit_id=_text(raw["semantic_unit_id"], "semantic_unit_id"),
        source_pr=source_pr,
        source_head=_text(raw["source_head"], "source_head"),
        source_path=_text(raw["source_path"], "source_path"),
        source_blob_sha=_text(raw["source_blob_sha"], "source_blob_sha"),
        source_locator=_text(raw["source_locator"], "source_locator"),
        phase_a_classification=CoverageClassification(raw["phase_a_classification"]),
        phase_a_disposition=CoverageDisposition(raw["phase_a_disposition"]),
        decision=MaterializationDecision(raw["decision"]),
        admission_status=MaterializationAdmissionStatus(raw["admission_status"]),
        architecture_layer=MaterializationArchitectureLayer(raw["architecture_layer"]),
        role_scope=MaterializationRoleScope(raw["role_scope"]),
        target_ref=_text(raw["target_ref"], "target_ref"),
        active_target_ref=_nullable_text(raw["active_target_ref"], "active_target_ref"),
        replacement_ref=_nullable_text(raw["replacement_ref"], "replacement_ref"),
        canonical_owner_unit_id=_nullable_text(
            raw["canonical_owner_unit_id"], "canonical_owner_unit_id"
        ),
        reason=_text(raw["reason"], "reason"),
    )


def load_materialization_map(path: str | Path) -> EmbodimentMaterializationMap:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = _mapping(payload, _MAP_KEYS, "materialization map")
    entries = raw["entries"]
    order = raw["canonical_order"]
    if type(entries) is not list or type(order) is not list:
        raise ValueError("entries and canonical_order must be arrays")
    if type(raw["deployment"]) is not bool:
        raise ValueError("deployment must be an exact bool")
    return EmbodimentMaterializationMap(
        map_id=_text(raw["map_id"], "map_id"),
        phase_a_matrix_id=_text(raw["phase_a_matrix_id"], "phase_a_matrix_id"),
        phase_a_matrix_sha256=_text(
            raw["phase_a_matrix_sha256"], "phase_a_matrix_sha256"
        ),
        entries=tuple(_load_entry(value) for value in entries),
        canonical_order=tuple(_text(value, "canonical_order") for value in order),
        scientific_disposition=_text(
            raw["scientific_disposition"], "scientific_disposition"
        ),
        subjectivity=_text(raw["subjectivity"], "subjectivity"),
        canonical_effect=_text(raw["canonical_effect"], "canonical_effect"),
        deployment=raw["deployment"],
    )


def _canonical_payload(value: EmbodimentMaterializationMap) -> dict[str, Any]:
    payload = asdict(value)
    payload["entries"] = sorted(
        payload["entries"],
        key=lambda item: (
            item["source_pr"], item["source_path"], item["semantic_unit_id"]
        ),
    )
    return payload


def materialization_map_hash(value: EmbodimentMaterializationMap) -> str:
    encoded = json.dumps(
        _canonical_payload(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _active_ownership_key(entry: MaterializationEntry) -> tuple[str, str, str]:
    return Path(entry.source_path).name, entry.source_blob_sha, entry.source_locator


def materialization_map_gate_counts(
    value: EmbodimentMaterializationMap,
) -> dict[str, int]:
    active = [
        entry
        for entry in value.entries
        if entry.admission_status is MaterializationAdmissionStatus.ACTIVE_VERIFIED
    ]
    active_keys = [_active_ownership_key(entry) for entry in active]
    return {
        "SEMANTIC_UNIT_COUNT": len(value.entries),
        "IMPLEMENT_EXISTING_TARGET_COUNT": sum(
            entry.decision is MaterializationDecision.IMPLEMENT_EXISTING_TARGET
            for entry in value.entries
        ),
        "EXTEND_EXISTING_TARGET_COUNT": sum(
            entry.decision is MaterializationDecision.EXTEND_EXISTING_TARGET
            for entry in value.entries
        ),
        "KEEP_DEFERRED_COUNT": sum(
            entry.decision is MaterializationDecision.KEEP_DEFERRED
            for entry in value.entries
        ),
        "SUPERSEDED_COUNT": sum(
            entry.decision is MaterializationDecision.SUPERSEDED
            for entry in value.entries
        ),
        "ARCHIVE_ONLY_COUNT": sum(
            entry.decision is MaterializationDecision.ARCHIVE_ONLY
            for entry in value.entries
        ),
        "NEEDS_NEW_TARGET_COUNT": sum(
            entry.decision is MaterializationDecision.NEEDS_NEW_TARGET
            for entry in value.entries
        ),
        "ACTIVE_VERIFIED_COUNT": len(active),
        "MISSING_MATERIALIZATION_DECISION_COUNT": 0,
        "DUPLICATE_ACTIVE_OWNERSHIP_COUNT": len(active_keys) - len(set(active_keys)),
    }


def _expected_role_scope(unit: SemanticUnitCoverage) -> MaterializationRoleScope:
    if unit.classification is CoverageClassification.SHARED_CORE:
        return MaterializationRoleScope.SHARED
    if unit.classification is CoverageClassification.EXTERNAL_DEFERRED:
        return MaterializationRoleScope.EXTERNAL
    if unit.source_pr == 191:
        return MaterializationRoleScope.AION_ASTRA
    if unit.source_pr == 192:
        return MaterializationRoleScope.CHATGPT_TEACHER
    raise ValueError("role-specific source has no exact role binding")


def _verify_source_binding(
    entry: MaterializationEntry,
    unit: SemanticUnitCoverage,
) -> None:
    if (
        entry.semantic_unit_id != unit.semantic_unit_id
        or entry.source_pr != unit.source_pr
        or entry.source_head != unit.source_head
        or entry.source_path != unit.source_path
        or entry.source_blob_sha != unit.source_blob_sha
        or entry.source_locator != unit.source_locator
        or entry.phase_a_classification is not unit.classification
        or entry.phase_a_disposition is not unit.disposition
    ):
        raise ValueError(f"source binding drift: {entry.semantic_unit_id}")


def _verify_decision(
    entry: MaterializationEntry,
    unit: SemanticUnitCoverage,
    entries_by_id: dict[str, MaterializationEntry],
) -> None:
    if unit.source_pr == 202:
        if (
            entry.decision is not MaterializationDecision.KEEP_DEFERRED
            or entry.admission_status is not MaterializationAdmissionStatus.KEPT_DEFERRED
            or entry.architecture_layer is not MaterializationArchitectureLayer.SENSORIMOTOR
        ):
            raise ValueError("PR #202 must remain exact deferred provenance in Phase B.1")

    if unit.disposition is CoverageDisposition.ADOPTED:
        if (
            entry.decision is not MaterializationDecision.IMPLEMENT_EXISTING_TARGET
            or entry.admission_status is not MaterializationAdmissionStatus.ACTIVE_VERIFIED
            or entry.active_target_ref != unit.active_target_ref
            or entry.target_ref != unit.target_ref
            or entry.replacement_ref is not None
            or entry.canonical_owner_unit_id is not None
        ):
            raise ValueError("adopted unit must reuse its exact active target")
        return

    if unit.disposition is CoverageDisposition.SUPERSEDED:
        if (
            entry.decision is not MaterializationDecision.SUPERSEDED
            or entry.admission_status
            is not MaterializationAdmissionStatus.EXCLUDED_SUPERSEDED
            or entry.active_target_ref is not None
            or entry.target_ref != unit.target_ref
            or entry.replacement_ref != unit.replacement_ref_if_superseded
            or entry.canonical_owner_unit_id is not None
        ):
            raise ValueError("superseded semantic unit cannot re-enter the active baseline")
        return

    if unit.disposition is CoverageDisposition.ARCHIVE_ONLY:
        if (
            entry.decision is not MaterializationDecision.ARCHIVE_ONLY
            or entry.admission_status is not MaterializationAdmissionStatus.ARCHIVED
            or entry.active_target_ref is not None
        ):
            raise ValueError("archive-only semantic unit cannot become active")
        return

    if unit.disposition is not CoverageDisposition.DEFERRED:
        raise ValueError("unsupported Phase A disposition")

    if entry.decision is MaterializationDecision.KEEP_DEFERRED:
        if (
            entry.admission_status is not MaterializationAdmissionStatus.KEPT_DEFERRED
            or entry.active_target_ref is not None
            or entry.target_ref != unit.target_ref
            or entry.replacement_ref is not None
            or entry.canonical_owner_unit_id is not None
        ):
            raise ValueError("deferred semantic unit cannot silently become active")
        return

    if entry.decision is MaterializationDecision.SUPERSEDED:
        owner_id = entry.canonical_owner_unit_id
        owner = entries_by_id.get(owner_id or "")
        if owner is None:
            raise ValueError("canonical owner does not exist")
        if (
            entry.admission_status
            is not MaterializationAdmissionStatus.EXCLUDED_SUPERSEDED
            or entry.active_target_ref is not None
            or entry.replacement_ref != f"semantic-unit:{owner_id}"
            or entry.target_ref != entry.replacement_ref
            or owner.decision is MaterializationDecision.SUPERSEDED
            or _active_ownership_key(entry) != _active_ownership_key(owner)
        ):
            raise ValueError("canonical owner binding is invalid")
        return

    raise ValueError("deferred semantic unit requires a separately reviewed admission")


def validate_materialization_map(
    value: EmbodimentMaterializationMap,
    matrix: EmbodimentArchiveCoverageMatrix,
) -> dict[str, int | str]:
    validate_coverage_matrix(matrix)
    if type(value) is not EmbodimentMaterializationMap:
        raise ValueError("materialization map must use the typed record")
    if value.map_id != "EMBODIMENT_MATERIALIZATION_MAP_v0.1":
        raise ValueError("unexpected materialization map id")
    if value.phase_a_matrix_id != matrix.matrix_id:
        raise ValueError("Phase A matrix id drift")
    if value.phase_a_matrix_sha256 != coverage_matrix_hash(matrix):
        raise ValueError("Phase A matrix hash drift")
    if value.canonical_order != CANONICAL_MATERIALIZATION_ORDER:
        raise ValueError("canonical order fields changed")
    if (
        value.scientific_disposition != "HOLD"
        or value.subjectivity != "NOT_ESTABLISHED"
        or value.canonical_effect != "NONE"
        or value.deployment is not False
    ):
        raise ValueError("scientific, canonical, and deployment boundaries changed")

    expected_ids = tuple(unit.semantic_unit_id for unit in matrix.semantic_units)
    actual_ids = tuple(entry.semantic_unit_id for entry in value.entries)
    if len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(expected_ids):
        raise ValueError("every Phase A semantic unit must be decided exactly once")
    if actual_ids != expected_ids:
        raise ValueError("materialization entries are not in canonical order")

    entries_by_id = {entry.semantic_unit_id: entry for entry in value.entries}
    for entry, unit in zip(value.entries, matrix.semantic_units, strict=True):
        if type(entry) is not MaterializationEntry:
            raise ValueError("materialization entries must use typed records")
        _verify_source_binding(entry, unit)
        expected_role = _expected_role_scope(unit)
        if entry.role_scope is not expected_role:
            if unit.classification is CoverageClassification.ROLE_SPECIFIC_EXTENSION:
                raise ValueError("role-specific semantic unit cannot leak into shared scope")
            raise ValueError("role scope does not match Phase A classification")
        if (
            unit.classification is CoverageClassification.ROLE_SPECIFIC_EXTENSION
            and entry.architecture_layer
            is MaterializationArchitectureLayer.SHARED_EMBODIMENT_CORE
        ):
            raise ValueError("role-specific semantic unit cannot leak into shared core")
        _verify_decision(entry, unit, entries_by_id)

    counts = materialization_map_gate_counts(value)
    if counts["MISSING_MATERIALIZATION_DECISION_COUNT"]:
        raise ValueError("missing materialization decision")
    if counts["DUPLICATE_ACTIVE_OWNERSHIP_COUNT"]:
        raise ValueError("duplicate active semantic ownership")
    return {"result": "PASS", **counts}


def validate_materialization_map_bindings(
    value: EmbodimentMaterializationMap,
    matrix: EmbodimentArchiveCoverageMatrix,
    repository_root: str | Path,
    *,
    git_executable: str = "git",
) -> dict[str, int | str]:
    report = validate_materialization_map(value, matrix)
    phase_a = validate_coverage_matrix_bindings(
        matrix, repository_root, git_executable=git_executable
    )
    return {
        **report,
        "SOURCE_BINDINGS": phase_a["SOURCE_BINDINGS"],
        "ACTIVE_TARGET_BINDINGS": phase_a["TARGET_BINDINGS"],
        "REPLACEMENT_BINDINGS": phase_a["REPLACEMENT_BINDINGS"],
        "SUPPORTING_ARTIFACT_BINDINGS": phase_a[
            "SUPPORTING_ARTIFACT_BINDINGS"
        ],
    }
