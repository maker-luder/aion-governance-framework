"""AION/Astra shared-genesis twin embodiment research candidate."""

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .runtime import TwinGenesisRuntime, TwinRuntimeState
from .runtime_binding import TwinRuntimeContexts, build_runtime_contexts
from .validation import ValidationError, validate_candidate
from .convergence import (
    AdoptionStatus, ArchiveDisposition, ConvergenceClassification,
    ConvergenceLedger, convergence_ledger_hash, load_convergence_ledger,
    validate_convergence_ledger,
)
from .shared_core import (
    ObservationDomain, ObservabilityClass, StaticBodyRegion,
    ObservationInterface, MotorInterface, PhysiologySystemInterface,
    SharedEmbodimentCore, build_shared_embodiment_core,
    shared_embodiment_core_hash, validate_shared_embodiment_core,
)
from .role_extensions import (
    RoleId, ExtensionCapability, RoleSpecificEmbodimentExtension,
    build_teacher_extension_manifest, validate_role_specific_extension,
)
from .active_baseline import (
    ActiveEmbodimentBaseline, build_active_embodiment_baseline,
    validate_active_embodiment_baseline,
)

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
    "AdoptionStatus", "ArchiveDisposition", "ConvergenceClassification",
    "ConvergenceLedger", "convergence_ledger_hash", "load_convergence_ledger",
    "validate_convergence_ledger", "ObservationDomain", "ObservabilityClass",
    "StaticBodyRegion", "ObservationInterface", "MotorInterface",
    "PhysiologySystemInterface", "SharedEmbodimentCore",
    "build_shared_embodiment_core", "shared_embodiment_core_hash",
    "validate_shared_embodiment_core", "RoleId", "ExtensionCapability",
    "RoleSpecificEmbodimentExtension", "build_teacher_extension_manifest",
    "validate_role_specific_extension", "ActiveEmbodimentBaseline",
    "build_active_embodiment_baseline", "validate_active_embodiment_baseline",
]
