"""AION/Astra shared-genesis twin embodiment research candidate."""

from .anthropometry import (
    AION_BODY_ID,
    ASTRA_BODY_ID,
    AnthropometryProfile,
    SyntheticGeometryRule,
    load_profile,
)
from .body_state import WholeBodySyntheticState, default_whole_body_state
from .capability_parity import (
    CapabilityParityRecord,
    build_capability_parity_record,
    validate_capability_parity,
)
from .continuity import (
    BodyRuntimeBinding,
    CrossSessionRetention,
    LongitudinalObservation,
    build_body_runtime_binding,
    build_cross_session_retention,
    observe_longitudinal,
)
from .dynamic_physiology import MalePhysiologyState, default_physiology_state
from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .probe import run_probe
from .reproductive_topology import (
    ReproductiveTopologyReference,
    build_reproductive_topology_reference,
    validate_reproductive_topology_parity,
)
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
    "CapabilityParityRecord",
    "build_capability_parity_record",
    "validate_capability_parity",
    "BodyRuntimeBinding",
    "CrossSessionRetention",
    "LongitudinalObservation",
    "build_body_runtime_binding",
    "build_cross_session_retention",
    "observe_longitudinal",
    "default_whole_body_state",
    "MalePhysiologyState",
    "default_physiology_state",
    "EmbodimentInstance",
    "EmbodimentTemplate",
    "SharedGenesisEvent",
    "run_probe",
    "ReproductiveTopologyReference",
    "build_reproductive_topology_reference",
    "validate_reproductive_topology_parity",
    "TwinGenesisRuntime",
    "TwinRuntimeState",
    "TwinRuntimeContexts",
    "build_runtime_contexts",
    "ValidationError",
    "validate_candidate",
]
