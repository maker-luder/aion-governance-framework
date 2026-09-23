"""Deferred role-specific provenance bound to exact v0.2 semantic units."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum

from .coverage_matrix import (
    ARCHIVE_HEADS_V0_2,
    CoverageClassification,
    CoverageDisposition,
    EmbodimentArchiveCoverageMatrix,
    SemanticUnitCoverage,
    coverage_matrix_hash,
    validate_coverage_matrix,
)
from .shared_core import SharedEmbodimentCore, shared_embodiment_core_hash
from .validation import deterministic_hash


class RoleId(StrEnum):
    AION = "AION"
    ASTRA = "ASTRA"
    CHATGPT_TEACHER = "CHATGPT_TEACHER"


@dataclass(frozen=True, slots=True)
class ExtensionCapability:
    capability_id: str
    semantic_unit_id: str
    source_path: str
    source_blob_sha: str
    classification: CoverageClassification
    disposition: CoverageDisposition
    active_target_ref: str | None = None


@dataclass(frozen=True, slots=True)
class RoleSpecificEmbodimentExtension:
    extension_id: str
    role: RoleId
    shared_core_sha256: str
    coverage_matrix_sha256: str
    source_pr: int
    source_head: str
    capabilities: tuple[ExtensionCapability, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


def _teacher_units(
    matrix: EmbodimentArchiveCoverageMatrix,
) -> tuple[SemanticUnitCoverage, ...]:
    validate_coverage_matrix(matrix)
    return tuple(
        unit
        for unit in matrix.semantic_units
        if unit.source_pr == 192
        and unit.classification is CoverageClassification.ROLE_SPECIFIC_EXTENSION
        and unit.disposition is CoverageDisposition.DEFERRED
    )


def _capability(unit: SemanticUnitCoverage) -> ExtensionCapability:
    return ExtensionCapability(
        capability_id=unit.semantic_unit_id,
        semantic_unit_id=unit.semantic_unit_id,
        source_path=unit.source_path,
        source_blob_sha=unit.source_blob_sha,
        classification=unit.classification,
        disposition=unit.disposition,
        active_target_ref=unit.active_target_ref,
    )


def build_teacher_extension_manifest(
    core: SharedEmbodimentCore,
    matrix: EmbodimentArchiveCoverageMatrix,
) -> RoleSpecificEmbodimentExtension:
    extension = RoleSpecificEmbodimentExtension(
        extension_id="CHATGPT_TEACHER_ARCHIVE_192",
        role=RoleId.CHATGPT_TEACHER,
        shared_core_sha256=shared_embodiment_core_hash(core),
        coverage_matrix_sha256=coverage_matrix_hash(matrix),
        source_pr=192,
        source_head=ARCHIVE_HEADS_V0_2[192],
        capabilities=tuple(_capability(unit) for unit in _teacher_units(matrix)),
    )
    validate_role_specific_extension(extension, core, matrix)
    return extension


def validate_role_specific_extension(
    extension: RoleSpecificEmbodimentExtension,
    core: SharedEmbodimentCore,
    matrix: EmbodimentArchiveCoverageMatrix,
) -> dict[str, str]:
    if type(extension) is not RoleSpecificEmbodimentExtension:
        raise ValueError("extension must use the typed record")
    if extension.shared_core_sha256 != shared_embodiment_core_hash(core):
        raise ValueError("shared core hash does not match extension")
    if extension.coverage_matrix_sha256 != coverage_matrix_hash(matrix):
        raise ValueError("coverage matrix hash does not match extension")
    if (
        extension.role is not RoleId.CHATGPT_TEACHER
        or extension.extension_id != "CHATGPT_TEACHER_ARCHIVE_192"
    ):
        raise ValueError("role-specific extension role binding mismatch")
    if (
        type(extension.source_pr) is not int
        or extension.source_pr != 192
        or extension.source_head != ARCHIVE_HEADS_V0_2[192]
    ):
        raise ValueError("archive source head does not match")
    if type(extension.capabilities) is not tuple or not extension.capabilities:
        raise ValueError("capabilities must be a nonempty tuple")

    ids: list[str] = []
    for item in extension.capabilities:
        if type(item) is not ExtensionCapability:
            raise ValueError("capability must be a typed record")
        for value, label in (
            (item.capability_id, "capability ID"),
            (item.semantic_unit_id, "semantic unit ID"),
            (item.source_path, "source path"),
            (item.source_blob_sha, "source blob SHA"),
        ):
            if type(value) is not str or not value.strip():
                raise ValueError(f"{label} is required")
        if item.capability_id != item.semantic_unit_id:
            raise ValueError("capability ID must equal its exact semantic unit ID")
        if item.classification is not CoverageClassification.ROLE_SPECIFIC_EXTENSION:
            raise ValueError("capability classification must remain role-specific")
        if item.disposition is CoverageDisposition.ADOPTED:
            if type(item.active_target_ref) is not str or not item.active_target_ref.strip():
                raise ValueError("adopted capability requires active target ref")
        elif item.disposition is CoverageDisposition.DEFERRED:
            if item.active_target_ref is not None:
                raise ValueError("deferred capability cannot claim an active target")
        else:
            raise ValueError("Teacher archive capabilities remain deferred")
        ids.append(item.capability_id)
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate capability IDs")

    expected = tuple(_capability(unit) for unit in _teacher_units(matrix))
    if extension.capabilities != expected:
        raise ValueError("archive capability provenance does not match v0.2 semantic units")
    if any(
        type(value) is not str or value != "NOT_ESTABLISHED"
        for value in (
            extension.subjectivity_conclusion,
            extension.phenomenal_experience_conclusion,
        )
    ):
        raise ValueError("subjectivity and phenomenal claims remain NOT_ESTABLISHED")
    if (
        type(extension.canonical_effect) is not str
        or extension.canonical_effect != "NONE"
    ):
        raise ValueError("extension cannot have canonical effect")
    if extension.deployment is not False:
        raise ValueError("extension cannot deploy")
    return {
        "result": "PASS",
        "extension_hash": deterministic_hash(asdict(extension)),
        "shared_core_sha256": extension.shared_core_sha256,
        "coverage_matrix_sha256": extension.coverage_matrix_sha256,
    }
