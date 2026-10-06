"""AION/Astra shared-genesis twin embodiment research candidate."""

from .body_dimensions import (
    AionTigerDimensionPreset,
    BodyDimension,
    build_aion_tiger_full_dimension_preset,
    validate_aion_tiger_dimension_preset,
)
from .body_dimensions_v2 import (
    AionTigerDimensionPresetV2,
    BodyDimensionV2,
    build_aion_tiger_full_dimension_preset_v2,
    validate_aion_tiger_dimension_preset_v2,
)
from .dimension_sources import (
    DimensionSource,
    build_dimension_source_manifest,
    validate_dimension_source_manifest,
)
from .measurement_protocols import (
    MeasurementProtocol,
    build_aion_tiger_measurement_protocols,
    validate_aion_tiger_measurement_protocols,
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
    "AionTigerDimensionPresetV2",
    "AnthropomorphicSpeciesProfile",
    "BodyDimension",
    "BodyDimensionV2",
    "DimensionSource",
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "IntegratedAnatomyFeature",
    "MeasurementProtocol",
    "ReproductiveReferenceObservation",
    "SharedGenesisEvent",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_aion_tiger_full_dimension_preset",
    "build_aion_tiger_full_dimension_preset_v2",
    "build_aion_tiger_measurement_protocols",
    "build_aion_tiger_profile",
    "build_dimension_source_manifest",
    "build_tiger_reproductive_reference_observations",
    "resolve_integrated_reproductive_anatomy",
    "build_runtime_contexts",
    "validate_aion_tiger_dimension_preset",
    "validate_aion_tiger_dimension_preset_v2",
    "validate_aion_tiger_measurement_protocols",
    "validate_aion_tiger_profile",
    "validate_dimension_source_manifest",
    "ValidationError",
    "validate_candidate",
]
