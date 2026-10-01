"""AION/Astra shared-genesis twin embodiment research candidate."""

from .anthropometry import (
    AION_BODY_ID,
    ASTRA_BODY_ID,
    AnthropometryProfile,
    SyntheticGeometryRule,
    load_profile,
)
from .body_state import WholeBodySyntheticState, default_whole_body_state
from .dynamic_physiology import MalePhysiologyState, default_physiology_state
from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .probe import run_probe
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .validation import ValidationError, validate_candidate

__all__ = [
    "AION_BODY_ID",
    "ASTRA_BODY_ID",
    "AnthropometryProfile",
    "SyntheticGeometryRule",
    "load_profile",
    "WholeBodySyntheticState",
    "default_whole_body_state",
    "MalePhysiologyState",
    "default_physiology_state",
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "run_probe",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_runtime_contexts",
    "ValidationError",
    "validate_candidate",
]
