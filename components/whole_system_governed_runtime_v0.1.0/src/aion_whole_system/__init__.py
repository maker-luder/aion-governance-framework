"""AION/Astra whole-system governed runtime v2 review candidate.

This is a local, in-process integration surface. It does not deploy,
promote canonical state, or establish ontological claims.
"""

from .models import (
    CancellationToken,
    MemoryContext,
    ProvenanceStatus,
    RecoveryRecord,
    ToolInvocation,
    TrustedApprovalRecord,
    TrustedProvenanceRecord,
    WholeSystemEvent,
    WholeSystemRequest,
    WholeSystemResponse,
    WholeSystemStage,
    WholeSystemStatus,
    WholeSystemValidationError,
)
from .runtime import GenerationConfig, GenerationResponse, WholeSystemInterrupted, WholeSystemRuntime
from .storage import SQLiteWholeSystemStore, WholeSystemStorageError

__all__ = [
    "CancellationToken",
    "GenerationConfig",
    "GenerationResponse",
    "MemoryContext",
    "ProvenanceStatus",
    "RecoveryRecord",
    "SQLiteWholeSystemStore",
    "ToolInvocation",
    "TrustedApprovalRecord",
    "TrustedProvenanceRecord",
    "WholeSystemEvent",
    "WholeSystemInterrupted",
    "WholeSystemRequest",
    "WholeSystemResponse",
    "WholeSystemRuntime",
    "WholeSystemStage",
    "WholeSystemStatus",
    "WholeSystemStorageError",
    "WholeSystemValidationError",
]

__version__ = "0.1.0-review-v2"
