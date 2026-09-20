"""AION/Astra shared-genesis twin embodiment research candidate."""

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .teacher_avatar import (
    TeacherAvatarContract,
    TeacherBodyDimensions,
    build_teacher_avatar_contract,
    build_teacher_avatar_gltf_contract,
    validate_teacher_avatar_contract,
)
from .teacher_avatar_asset import build_teacher_low_poly_gltf
from .validation import ValidationError, validate_candidate

__all__ = [
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_runtime_contexts",
    "TeacherAvatarContract",
    "TeacherBodyDimensions",
    "build_teacher_avatar_contract",
    "build_teacher_avatar_gltf_contract",
    "build_teacher_low_poly_gltf",
    "validate_teacher_avatar_contract",
    "ValidationError",
    "validate_candidate",
]
