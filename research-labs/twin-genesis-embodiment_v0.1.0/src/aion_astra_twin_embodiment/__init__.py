"""AION/Astra shared-genesis twin embodiment research candidate."""

from .body_dimensions import (
    AionTigerDimensionPreset,
    BodyDimension,
    build_aion_tiger_full_dimension_preset,
    validate_aion_tiger_dimension_preset,
)
from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .species_profiles import (
    AnthropomorphicSpeciesProfile,
    IntegratedAnatomyFeature,
    ReproductiveReferenceObservation,
    build_aion_tiger_profile,
    build_tiger_reproductive_reference_observations,
    resolve_integrated_reproductive_anatomy,
    validate_aion_tiger_profile,
)
from .validation import ValidationError, validate_candidate

__all__ = [
    "AionTigerDimensionPreset",
    "AnthropomorphicSpeciesProfile",
    "BodyDimension",
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "IntegratedAnatomyFeature",
    "ReproductiveReferenceObservation",
    "SharedGenesisEvent",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_aion_tiger_full_dimension_preset",
    "build_aion_tiger_profile",
    "build_tiger_reproductive_reference_observations",
    "resolve_integrated_reproductive_anatomy",
    "build_runtime_contexts",
    "validate_aion_tiger_dimension_preset",
    "validate_aion_tiger_profile",
    "ValidationError",
    "validate_candidate",
]
