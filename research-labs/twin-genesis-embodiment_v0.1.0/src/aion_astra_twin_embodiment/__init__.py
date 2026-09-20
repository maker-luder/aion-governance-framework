"""AION/Astra shared-genesis twin embodiment research candidate."""

from .body_profiles import (
    BodyProfileCandidate,
    BodyProfileValidationError,
    DimensionSpec,
    PoseDeformationTestCandidate,
    load_body_profile,
    load_pose_test,
    validate_body_profile,
    validate_pose_test,
    validate_profile_pair,
)
from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .validation import ValidationError, validate_candidate

__all__ = [
    "BodyProfileCandidate",
    "BodyProfileValidationError",
    "DimensionSpec",
    "PoseDeformationTestCandidate",
    "load_body_profile",
    "load_pose_test",
    "validate_body_profile",
    "validate_pose_test",
    "validate_profile_pair",
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_runtime_contexts",
    "ValidationError",
    "validate_candidate",
]
