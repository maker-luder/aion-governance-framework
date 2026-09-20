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
    "ValidationError",
    "validate_candidate",
]
