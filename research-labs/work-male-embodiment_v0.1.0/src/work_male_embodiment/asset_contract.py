from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class AssetFormat(str, Enum):
    GLTF = "gltf"
    GLB = "glb"


class VerificationState(str, Enum):
    REQUIRED_UNVERIFIED = "REQUIRED_UNVERIFIED"
    CANDIDATE_PRESENT = "CANDIDATE_PRESENT"
    VERIFIED = "VERIFIED"


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


@dataclass(frozen=True)
class RigNodeRequirement:
    node_id: str
    joint_limits_assigned: bool = False

    def __post_init__(self) -> None:
        if self.node_id not in _REQUIRED_RIG_NODES:
            raise ValueError(f"unknown required rig node: {self.node_id}")


@dataclass(frozen=True)
class WorkAssetEngineeringContract:
    required_measurement_ids: tuple[str, ...]
    rig_nodes: tuple[RigNodeRequirement, ...]
    external_geometry_nodes: tuple[str, ...]
    collision_geometry_required: bool = True
    mass_properties_required: bool = True
    skinning_required: bool = True
    prepuce_mobility_geometry_required: bool = True

    def __post_init__(self) -> None:
        if len(self.required_measurement_ids) != 67:
            raise ValueError("asset contract must retain all 67 selected measurements")
        if len(set(self.required_measurement_ids)) != 67:
            raise ValueError("duplicate measurement ids in asset contract")
        if tuple(node.node_id for node in self.rig_nodes) != _REQUIRED_RIG_NODES:
            raise ValueError("rig contract changed")
        if self.external_geometry_nodes != _REQUIRED_EXTERNAL_GEOMETRY_NODES:
            raise ValueError("external male-form geometry contract changed")


@dataclass(frozen=True)
class AssetCandidateEvidence:
    status: VerificationState = VerificationState.REQUIRED_UNVERIFIED
    asset_format: AssetFormat | None = None
    asset_path: str | None = None
    sha256: str | None = None
    measurement_ids_verified: tuple[str, ...] = ()
    rig_nodes_present: tuple[str, ...] = ()
    joint_limits_verified: bool = False
    collision_geometry_verified: bool = False
    mass_properties_verified: bool = False
    skinning_verified: bool = False
    external_geometry_nodes_present: tuple[str, ...] = ()
    prepuce_mobility_geometry_verified: bool = False
    actual_3d_mesh: bool = False
    as_built_verified: bool = False

    def __post_init__(self) -> None:
        if self.sha256 is not None and _SHA256_RE.fullmatch(self.sha256) is None:
            raise ValueError("asset sha256 must be 64 lowercase hex characters")
        if self.status is VerificationState.REQUIRED_UNVERIFIED:
            if any(
                (
                    self.asset_format is not None,
                    self.asset_path is not None,
                    self.sha256 is not None,
                    bool(self.measurement_ids_verified),
                    bool(self.rig_nodes_present),
                    self.joint_limits_verified,
                    self.collision_geometry_verified,
                    self.mass_properties_verified,
                    self.skinning_verified,
                    bool(self.external_geometry_nodes_present),
                    self.prepuce_mobility_geometry_verified,
                    self.actual_3d_mesh,
                    self.as_built_verified,
                )
            ):
                raise ValueError("unverified asset cannot carry implementation evidence")
        if self.actual_3d_mesh and (
            self.asset_format is None or self.asset_path is None or self.sha256 is None
        ):
            raise ValueError("mesh claim requires format, path, and sha256")
        if self.as_built_verified and not self.actual_3d_mesh:
            raise ValueError("as-built verification requires an actual mesh")


def build_asset_contract(measurement_ids: tuple[str, ...]) -> WorkAssetEngineeringContract:
    return WorkAssetEngineeringContract(
        required_measurement_ids=measurement_ids,
        rig_nodes=tuple(RigNodeRequirement(node_id=node_id) for node_id in _REQUIRED_RIG_NODES),
        external_geometry_nodes=_REQUIRED_EXTERNAL_GEOMETRY_NODES,
    )


def verify_asset_candidate(
    contract: WorkAssetEngineeringContract,
    evidence: AssetCandidateEvidence,
) -> tuple[bool, tuple[str, ...]]:
    missing: list[str] = []
    if not evidence.actual_3d_mesh:
        missing.append("actual_3d_mesh")
    if set(evidence.measurement_ids_verified) != set(contract.required_measurement_ids):
        missing.append("67_measurements_verified")
    if set(evidence.rig_nodes_present) != {node.node_id for node in contract.rig_nodes}:
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
    if (
        contract.prepuce_mobility_geometry_required
        and not evidence.prepuce_mobility_geometry_verified
    ):
        missing.append("prepuce_mobility_geometry")
    return (not missing and evidence.as_built_verified, tuple(missing))
