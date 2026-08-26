"""AION/Astra shared agent execution substrate boundary v0.1.0."""

from .dispatch import (
    RECEIPT_FILENAME,
    NativeDispatchOutcome,
    SubstrateDispatcher,
    SubstratePolicyHold,
    dispatch_native_execution,
)
from .dsh import (
    DSH_PROFILE_ID,
    DSH_RELEASE_LABEL,
    DSH_UPSTREAM_REF,
    DSH_UPSTREAM_REPOSITORY,
    fork_lineage,
    normalize_trajectory as normalize_dsh_trajectory,
    profile as dsh_profile,
    team_snapshot,
)
from .durable import (
    EVENT_LOG_FILENAME,
    EXECUTION_EVIDENCE_FILENAME,
    DurableLogSummary,
    verify_execution_event_log,
    verify_execution_evidence,
)
from .evidence import (
    materialize_research_evidence_bytes,
    materialize_research_evidence_record,
    trajectory_digest,
)
from .models import (
    AgentId,
    Capability,
    Decision,
    EventFamily,
    ForkLineage,
    NormalizedEvent,
    PolicyDecision,
    PolicyRequest,
    RuntimeBinding,
    SubstrateError,
    SubstrateProfile,
    TeamSnapshot,
)
from .native import NATIVE_PROFILE_ID, normalize_trajectory as normalize_native_trajectory
from .policy import evaluate
from .registry import (
    NATIVE_ADAPTER_ID,
    AdapterRegistration,
    AdapterRegistry,
    AdapterRegistryError,
    build_default_registry,
)

__all__ = [
    "AdapterRegistration",
    "AdapterRegistry",
    "AdapterRegistryError",
    "AgentId",
    "Capability",
    "DSH_PROFILE_ID",
    "DSH_RELEASE_LABEL",
    "DSH_UPSTREAM_REF",
    "DSH_UPSTREAM_REPOSITORY",
    "Decision",
    "DurableLogSummary",
    "EVENT_LOG_FILENAME",
    "EXECUTION_EVIDENCE_FILENAME",
    "EventFamily",
    "ForkLineage",
    "NATIVE_ADAPTER_ID",
    "NATIVE_PROFILE_ID",
    "NativeDispatchOutcome",
    "NormalizedEvent",
    "PolicyDecision",
    "PolicyRequest",
    "RECEIPT_FILENAME",
    "RuntimeBinding",
    "SubstrateDispatcher",
    "SubstrateError",
    "SubstratePolicyHold",
    "SubstrateProfile",
    "TeamSnapshot",
    "build_default_registry",
    "dispatch_native_execution",
    "dsh_profile",
    "evaluate",
    "fork_lineage",
    "materialize_research_evidence_bytes",
    "materialize_research_evidence_record",
    "normalize_dsh_trajectory",
    "normalize_native_trajectory",
    "team_snapshot",
    "trajectory_digest",
    "verify_execution_event_log",
    "verify_execution_evidence",
]
