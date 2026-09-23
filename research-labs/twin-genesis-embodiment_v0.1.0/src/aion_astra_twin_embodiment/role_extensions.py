"""Deferred role-specific embodiment provenance; no archive runtime is imported."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum

from .convergence import ARCHIVE_HEADS, AdoptionStatus
from .shared_core import SharedEmbodimentCore, shared_embodiment_core_hash
from .validation import deterministic_hash


class RoleId(StrEnum):
    AION = "AION"
    ASTRA = "ASTRA"
    CHATGPT_TEACHER = "CHATGPT_TEACHER"


@dataclass(frozen=True, slots=True)
class ExtensionCapability:
    capability_id: str
    source_path_or_semantic_unit: str
    adoption_status: AdoptionStatus
    active_target_ref: str | None = None


@dataclass(frozen=True, slots=True)
class RoleSpecificEmbodimentExtension:
    extension_id: str
    role: RoleId
    shared_core_sha256: str
    source_pr: int
    source_head: str
    capabilities: tuple[ExtensionCapability, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


_TEACHER_CAPABILITIES = (
    ("TEACHER_ANTHROPOMETRY_62_MEASURE", "teacher_anthropometry.py :: 62-measure profile"),
    ("TEACHER_SIGNAL_CHANNELS", "teacher_body_channels.py :: Teacher channel instances"),
    ("TEACHER_MOTOR_SCHEMA", "teacher_body_channels.py :: Teacher motor schema"),
    ("TEACHER_BODY_MODEL", "teacher_body_model.py :: Teacher body model"),
    ("TEACHER_PHYSIOLOGY_OBSERVABILITY", "teacher_physiology_observability.py :: Teacher bindings"),
    ("TEACHER_RUNTIME_BINDING", "teacher_body_runtime.py :: Teacher runtime binding"),
    ("TEACHER_CALIBRATION_ADAPTATION", "teacher_body_dynamics.py :: calibration/adaptation"),
    ("TEACHER_CROSS_SESSION_RETENTION", "teacher_longitudinal.py :: cross-session retention"),
    ("TEACHER_LONGITUDINAL_TRAJECTORY", "teacher_longitudinal.py :: trajectory"),
    ("TEACHER_AVATAR_ASSET_FAMILY", "teacher_avatar.py :: avatar assets"),
    ("TEACHER_DETAILED_PHYSIOLOGY_GEOMETRY", "teacher_genital_geometry.py :: detailed geometry"),
)


def build_teacher_extension_manifest(
    core: SharedEmbodimentCore,
) -> RoleSpecificEmbodimentExtension:
    extension = RoleSpecificEmbodimentExtension(
        extension_id="CHATGPT_TEACHER_ARCHIVE_192",
        role=RoleId.CHATGPT_TEACHER,
        shared_core_sha256=shared_embodiment_core_hash(core),
        source_pr=192,
        source_head=ARCHIVE_HEADS[192],
        capabilities=tuple(
            ExtensionCapability(capability_id, source_ref, AdoptionStatus.DEFERRED)
            for capability_id, source_ref in _TEACHER_CAPABILITIES
        ),
    )
    validate_role_specific_extension(extension, core)
    return extension


def validate_role_specific_extension(
    extension: RoleSpecificEmbodimentExtension,
    core: SharedEmbodimentCore,
) -> dict[str, str]:
    if type(extension) is not RoleSpecificEmbodimentExtension:
        raise ValueError("extension must use the typed record")
    if extension.shared_core_sha256 != shared_embodiment_core_hash(core):
        raise ValueError("shared core hash does not match extension")
    if extension.role is not RoleId.CHATGPT_TEACHER or extension.extension_id != "CHATGPT_TEACHER_ARCHIVE_192":
        raise ValueError("role-specific extension role binding mismatch")
    if type(extension.source_pr) is not int or extension.source_pr != 192 or extension.source_head != ARCHIVE_HEADS[192]:
        raise ValueError("archive source head does not match")
    if type(extension.capabilities) is not tuple or not extension.capabilities:
        raise ValueError("capabilities must be a nonempty tuple")
    ids: list[str] = []
    for item in extension.capabilities:
        if type(item) is not ExtensionCapability:
            raise ValueError("capability must be a typed record")
        if type(item.capability_id) is not str or not item.capability_id.strip():
            raise ValueError("capability ID is required")
        if type(item.source_path_or_semantic_unit) is not str or not item.source_path_or_semantic_unit.strip():
            raise ValueError("capability source is required")
        if type(item.adoption_status) is not AdoptionStatus:
            raise ValueError("capability adoption status must use the exact enum")
        if item.adoption_status is AdoptionStatus.ADOPTED:
            if type(item.active_target_ref) is not str or not item.active_target_ref.strip():
                raise ValueError("adopted capability requires active target ref")
        elif item.active_target_ref is not None:
            raise ValueError("deferred capability cannot claim an active target")
        ids.append(item.capability_id)
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate capability IDs")
    if {item.capability_id: item.source_path_or_semantic_unit for item in extension.capabilities} != dict(_TEACHER_CAPABILITIES):
        raise ValueError("archive capability provenance does not match #192")
    if any(item.adoption_status is not AdoptionStatus.DEFERRED for item in extension.capabilities):
        raise ValueError("archive capabilities remain deferred in this convergence")
    if any(type(value) is not str or value != "NOT_ESTABLISHED" for value in (
        extension.subjectivity_conclusion, extension.phenomenal_experience_conclusion,
    )):
        raise ValueError("subjectivity and phenomenal claims remain NOT_ESTABLISHED")
    if type(extension.canonical_effect) is not str or extension.canonical_effect != "NONE":
        raise ValueError("extension cannot have canonical effect")
    if extension.deployment is not False:
        raise ValueError("extension cannot deploy")
    return {"result": "PASS", "extension_hash": deterministic_hash(asdict(extension)),
            "shared_core_sha256": extension.shared_core_sha256}
