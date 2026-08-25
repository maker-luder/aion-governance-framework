"""AION/Astra shared agent execution substrate boundary v0.1.0."""

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
from .native import normalize_trajectory as normalize_native_trajectory
from .policy import evaluate

__all__ = [
    "AgentId",
    "Capability",
    "DSH_PROFILE_ID",
    "DSH_RELEASE_LABEL",
    "DSH_UPSTREAM_REF",
    "DSH_UPSTREAM_REPOSITORY",
    "Decision",
    "EventFamily",
    "ForkLineage",
    "NormalizedEvent",
    "PolicyDecision",
    "PolicyRequest",
    "RuntimeBinding",
    "SubstrateError",
    "SubstrateProfile",
    "TeamSnapshot",
    "dsh_profile",
    "evaluate",
    "fork_lineage",
    "materialize_research_evidence_bytes",
    "materialize_research_evidence_record",
    "normalize_dsh_trajectory",
    "normalize_native_trajectory",
    "team_snapshot",
    "trajectory_digest",
]
