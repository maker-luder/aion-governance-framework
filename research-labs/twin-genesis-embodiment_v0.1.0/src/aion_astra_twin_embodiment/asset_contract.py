from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_RIG_NODES = (
    "root","pelvis","spine","chest","neck","head",
    "left_upper_arm","left_forearm","left_hand","right_upper_arm","right_forearm","right_hand",
    "left_thigh","left_shin","left_foot","right_thigh","right_shin","right_foot",
)
_REQUIRED_EXTERNAL_GEOMETRY_NODES = ("penis","glans","prepuce","frenulum","scrotum")


class AssetFormat(str, Enum):
    GLTF = "gltf"
    GLB = "glb"


class VerificationState(str, Enum):
    REQUIRED_UNVERIFIED = "REQUIRED_UNVERIFIED"
    PROCEDURAL_RIG_REFERENCE = "PROCEDURAL_RIG_REFERENCE"
    REFERENCE_MESH_CANDIDATE = "REFERENCE_MESH_CANDIDATE"
    AS_BUILT_VERIFIED = "AS_BUILT_VERIFIED"


@dataclass(frozen=True, slots=True)
class AssetEngineeringContract:
    agent_id: str
    body_id: str
    required_measurement_ids: tuple[str, ...]
    rig_nodes: tuple[str, ...] = _REQUIRED_RIG_NODES
    external_geometry_nodes: tuple[str, ...] = _REQUIRED_EXTERNAL_GEOMETRY_NODES
    joint_limits_required: bool = True
    collision_geometry_required: bool = True
    mass_properties_required: bool = True
    skinning_required: bool = True
    soft_tissue_deformation_required: bool = True
    prepuce_mobility_geometry_required: bool = True

    def __post_init__(self) -> None:
        if self.agent_id not in {"AION", "ASTRA"}:
            raise ValueError("unknown agent")
        if len(self.required_measurement_ids) != 67 or len(set(self.required_measurement_ids)) != 67:
            raise ValueError("asset contract requires all 67 measurements")
        if self.rig_nodes != _REQUIRED_RIG_NODES:
            raise ValueError("rig contract drift")
        if self.external_geometry_nodes != _REQUIRED_EXTERNAL_GEOMETRY_NODES:
            raise ValueError("external geometry contract drift")


@dataclass(frozen=True, slots=True)
class AssetCandidateEvidence:
    status: VerificationState = VerificationState.REQUIRED_UNVERIFIED
    asset_format: AssetFormat | None = None
    asset_path: str | None = None
    sha256: str | None = None
    rig_nodes_present: tuple[str, ...] = ()
    external_geometry_nodes_present: tuple[str, ...] = ()
    measurement_ids_geometry_verified: tuple[str, ...] = ()
    joint_limits_verified: bool = False
    collision_geometry_verified: bool = False
    mass_properties_verified: bool = False
    skinning_verified: bool = False
    soft_tissue_deformation_verified: bool = False
    prepuce_mobility_geometry_verified: bool = False
    actual_3d_mesh: bool = False
    as_built_verified: bool = False
    physical_body_present: bool = False

    def __post_init__(self) -> None:
        if self.sha256 is not None and _SHA256_RE.fullmatch(self.sha256) is None:
            raise ValueError("invalid sha256")
        if self.status is VerificationState.PROCEDURAL_RIG_REFERENCE:
            if self.asset_format is not AssetFormat.GLTF or self.asset_path is None or self.sha256 is None:
                raise ValueError("procedural rig requires glTF path/hash")
            if self.actual_3d_mesh or self.as_built_verified or self.physical_body_present:
                raise ValueError("procedural rig cannot be promoted to mesh/as-built/physical body")
        if self.physical_body_present:
            raise ValueError("physical body is not established")
        if self.as_built_verified and not self.actual_3d_mesh:
            raise ValueError("as-built verification requires actual mesh")


def verify_asset_candidate(
    contract: AssetEngineeringContract,
    evidence: AssetCandidateEvidence,
) -> tuple[bool, tuple[str, ...]]:
    missing: list[str] = []
    if not evidence.actual_3d_mesh:
        missing.append("actual_3d_mesh")
    if set(evidence.measurement_ids_geometry_verified) != set(contract.required_measurement_ids):
        missing.append("67_measurements_geometry_verified")
    if set(evidence.rig_nodes_present) != set(contract.rig_nodes):
        missing.append("rig_nodes")
    if set(evidence.external_geometry_nodes_present) != set(contract.external_geometry_nodes):
        missing.append("external_geometry_nodes")
    for required, ok, label in (
        (contract.joint_limits_required, evidence.joint_limits_verified, "joint_limits"),
        (contract.collision_geometry_required, evidence.collision_geometry_verified, "collision_geometry"),
        (contract.mass_properties_required, evidence.mass_properties_verified, "mass_properties"),
        (contract.skinning_required, evidence.skinning_verified, "skinning"),
        (contract.soft_tissue_deformation_required, evidence.soft_tissue_deformation_verified, "soft_tissue_deformation"),
        (contract.prepuce_mobility_geometry_required, evidence.prepuce_mobility_geometry_verified, "prepuce_mobility_geometry"),
    ):
        if required and not ok:
            missing.append(label)
    return (not missing and evidence.as_built_verified, tuple(missing))
