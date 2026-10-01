from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_RIG_NODES = (
    "root",
    "pelvis",
    "spine",
    "chest",
    "neck",
    "head",
    "left_upper_arm",
    "left_forearm",
    "left_hand",
    "right_upper_arm",
    "right_forearm",
    "right_hand",
    "left_thigh",
    "left_shin",
    "left_foot",
    "right_thigh",
    "right_shin",
    "right_foot",
)
_REQUIRED_EXTERNAL_GEOMETRY_NODES = (
    "penis",
    "glans",
    "prepuce",
    "frenulum",
    "scrotum",
)


class AssetFormat(str, Enum):
    GLTF = "gltf"
    GLB = "glb"


class VerificationState(str, Enum):
    REQUIRED_UNVERIFIED = "REQUIRED_UNVERIFIED"
    PROCEDURAL_RIG_REFERENCE = "PROCEDURAL_RIG_REFERENCE"
    MESH_CANDIDATE = "MESH_CANDIDATE"
    AS_BUILT_VERIFIED = "AS_BUILT_VERIFIED"


@dataclass(frozen=True, slots=True)
class CodexAssetEngineeringContract:
    required_measurement_ids: tuple[str, ...]
    rig_nodes: tuple[str, ...] = _REQUIRED_RIG_NODES
    external_geometry_nodes: tuple[str, ...] = _REQUIRED_EXTERNAL_GEOMETRY_NODES
    joint_limits_required: bool = True
    collision_geometry_required: bool = True
    mass_properties_required: bool = True
    skinning_required: bool = True
    prepuce_mobility_geometry_required: bool = True

    def __post_init__(self) -> None:
        if len(self.required_measurement_ids) != 67 or len(set(self.required_measurement_ids)) != 67:
            raise ValueError("asset contract must retain all 67 selected measurements")
        if self.rig_nodes != _REQUIRED_RIG_NODES:
            raise ValueError("rig contract changed")
        if self.external_geometry_nodes != _REQUIRED_EXTERNAL_GEOMETRY_NODES:
            raise ValueError("external geometry contract changed")


@dataclass(frozen=True, slots=True)
class AssetCandidateEvidence:
    status: VerificationState = VerificationState.REQUIRED_UNVERIFIED
    asset_format: AssetFormat | None = None
    asset_path: str | None = None
    sha256: str | None = None
    measurement_ids_verified: tuple[str, ...] = ()
    rig_nodes_present: tuple[str, ...] = ()
    external_geometry_nodes_present: tuple[str, ...] = ()
    joint_limits_verified: bool = False
    collision_geometry_verified: bool = False
    mass_properties_verified: bool = False
    skinning_verified: bool = False
    prepuce_mobility_geometry_verified: bool = False
    actual_3d_mesh: bool = False
    as_built_verified: bool = False
    physical_body_present: bool = False

    def __post_init__(self) -> None:
        if self.sha256 is not None and _SHA256_RE.fullmatch(self.sha256) is None:
            raise ValueError("asset sha256 must be lowercase hex")
        if self.status is VerificationState.REQUIRED_UNVERIFIED:
            if any(
                (
                    self.asset_format is not None,
                    self.asset_path is not None,
                    self.sha256 is not None,
                    bool(self.measurement_ids_verified),
                    bool(self.rig_nodes_present),
                    bool(self.external_geometry_nodes_present),
                    self.joint_limits_verified,
                    self.collision_geometry_verified,
                    self.mass_properties_verified,
                    self.skinning_verified,
                    self.prepuce_mobility_geometry_verified,
                    self.actual_3d_mesh,
                    self.as_built_verified,
                    self.physical_body_present,
                )
            ):
                raise ValueError("unverified asset cannot carry evidence")
        if self.status is VerificationState.PROCEDURAL_RIG_REFERENCE:
            if self.asset_format is not AssetFormat.GLTF or self.asset_path is None or self.sha256 is None:
                raise ValueError("procedural rig reference requires glTF path and hash")
            if self.actual_3d_mesh or self.as_built_verified or self.physical_body_present:
                raise ValueError("rig reference cannot become physical/as-built mesh")
        if self.actual_3d_mesh and (
            self.asset_format is None or self.asset_path is None or self.sha256 is None
        ):
            raise ValueError("mesh claim requires format/path/hash")
        if self.as_built_verified and not self.actual_3d_mesh:
            raise ValueError("as-built requires actual mesh")
        if self.physical_body_present:
            raise ValueError("physical Codex body is not established")


def build_asset_contract(
    measurement_ids: tuple[str, ...],
) -> CodexAssetEngineeringContract:
    return CodexAssetEngineeringContract(required_measurement_ids=measurement_ids)


def verify_asset_candidate(
    contract: CodexAssetEngineeringContract,
    evidence: AssetCandidateEvidence,
) -> tuple[bool, tuple[str, ...]]:
    missing: list[str] = []
    if not evidence.actual_3d_mesh:
        missing.append("actual_3d_mesh")
    if set(evidence.measurement_ids_verified) != set(contract.required_measurement_ids):
        missing.append("67_measurements_geometry_verified")
    if set(evidence.rig_nodes_present) != set(contract.rig_nodes):
        missing.append("rig_nodes")
    if not evidence.joint_limits_verified:
        missing.append("joint_limits")
    if contract.collision_geometry_required and not evidence.collision_geometry_verified:
        missing.append("collision_geometry")
    if contract.mass_properties_required and not evidence.mass_properties_verified:
        missing.append("mass_properties")
    if contract.skinning_required and not evidence.skinning_verified:
        missing.append("skinning")
    if set(evidence.external_geometry_nodes_present) != set(contract.external_geometry_nodes):
        missing.append("external_geometry_nodes")
    if contract.prepuce_mobility_geometry_required and not evidence.prepuce_mobility_geometry_verified:
        missing.append("prepuce_mobility_geometry")
    if evidence.physical_body_present:
        missing.append("physical_body_boundary_violation")
    return (not missing and evidence.as_built_verified, tuple(missing))
