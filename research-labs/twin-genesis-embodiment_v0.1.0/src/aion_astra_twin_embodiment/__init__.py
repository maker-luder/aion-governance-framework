"""AION/Astra shared-genesis twin embodiment research candidate."""

from .governance_epistemics import (
    AbsenceAssessment,
    CapabilityGovernanceState,
    ExternalActionDecision,
    assess_observed_absence,
    build_capability_governance_state,
    evaluate_external_action,
    validate_capability_governance_state,
)
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
    "AbsenceAssessment",
    "CapabilityGovernanceState",
    "ExternalActionDecision",
    "assess_observed_absence",
    "build_capability_governance_state",
    "evaluate_external_action",
    "validate_capability_governance_state",
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
