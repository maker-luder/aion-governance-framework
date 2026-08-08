"""AION/Astra shared-genesis twin embodiment research candidate."""

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .validation import ValidationError, validate_candidate

__all__ = [
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
