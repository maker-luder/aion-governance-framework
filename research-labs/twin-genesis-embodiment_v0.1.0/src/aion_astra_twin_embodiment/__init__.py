"""AION/Astra shared-genesis twin embodiment research candidate."""

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .physiology import (
    REFERENCE_FUNCTIONAL_COMPLETENESS,
    AdultMalePhysiologyReference,
    PhysiologySystemReference,
    build_adult_male_physiology_reference,
    validate_adult_male_physiology_reference,
    validate_physiology_parity,
)
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .teacher_avatar import (
    TeacherAvatarContract,
    TeacherBodyDimensions,
    build_teacher_avatar_contract,
    build_teacher_avatar_gltf_contract,
    validate_teacher_avatar_contract,
)
from .teacher_avatar_asset import build_teacher_low_poly_glb, build_teacher_low_poly_gltf
from .teacher_avatar_bundle import (
    TeacherReferenceBundleReceipt,
    build_teacher_reference_bundle_bytes,
    write_teacher_reference_bundle,
)
from .teacher_avatar_continuous import (
    ContinuousReferenceMesh,
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_gltf,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
    validate_teacher_continuous_reference_glb,
    validate_teacher_continuous_reference_gltf,
)
from .teacher_avatar_lod import (
    TeacherLodReference,
    build_teacher_lod_manifest,
    build_teacher_lod_references,
    validate_teacher_lod_references,
)
from .teacher_avatar_physics import (
    CollisionProxy,
    TeacherCollisionProfile,
    build_teacher_collision_profile,
    validate_teacher_collision_profile,
)
from .teacher_avatar_validation import (
    TeacherAvatarAssetValidationError,
    build_teacher_asset_manifest,
    validate_teacher_low_poly_glb,
    validate_teacher_low_poly_gltf,
)
from .validation import ValidationError, validate_candidate

__all__ = [
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "PhysiologySystemReference",
    "AdultMalePhysiologyReference",
    "REFERENCE_FUNCTIONAL_COMPLETENESS",
    "build_adult_male_physiology_reference",
    "validate_adult_male_physiology_reference",
    "validate_physiology_parity",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_runtime_contexts",
    "TeacherAvatarContract",
    "TeacherBodyDimensions",
    "build_teacher_avatar_contract",
    "build_teacher_avatar_gltf_contract",
    "build_teacher_low_poly_gltf",
    "build_teacher_low_poly_glb",
    "ContinuousReferenceMesh",
    "build_teacher_continuous_reference_mesh",
    "build_teacher_continuous_reference_gltf",
    "build_teacher_continuous_reference_glb",
    "TeacherReferenceBundleReceipt",
    "build_teacher_reference_bundle_bytes",
    "write_teacher_reference_bundle",
    "validate_teacher_continuous_reference",
    "validate_teacher_continuous_reference_gltf",
    "validate_teacher_continuous_reference_glb",
    "TeacherLodReference",
    "build_teacher_lod_references",
    "build_teacher_lod_manifest",
    "validate_teacher_lod_references",
    "CollisionProxy",
    "TeacherCollisionProfile",
    "build_teacher_collision_profile",
    "validate_teacher_collision_profile",
    "TeacherAvatarAssetValidationError",
    "build_teacher_asset_manifest",
    "validate_teacher_low_poly_gltf",
    "validate_teacher_low_poly_glb",
    "validate_teacher_avatar_contract",
    "ValidationError",
    "validate_candidate",
]
