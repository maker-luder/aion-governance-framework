"""Bounded owner-governed execution infrastructure for AION/Astra candidates.

This package provides shared execution mechanics. It has no canonical write,
deployment, identity-mutation, or subjectivity-establishing capability.
"""

from .engine import AstraRuntime, BoundedExecutionEngine
from .interop import (
    ErrorCategory,
    ErrorEnvelope,
    InteropError,
    canonical_json_bytes,
    canonical_json_text,
    parse_strict_json,
    sha256_canonical,
    validate_identifier,
    validate_timestamp,
    validate_version,
)
from .models import IndividualRuntimeContext, RunResult, RunStatus, TaskSpec

__all__ = [
    "AstraRuntime",
    "BoundedExecutionEngine",
    "IndividualRuntimeContext",
    "RunResult",
    "RunStatus",
    "TaskSpec",
    "ErrorCategory",
    "ErrorEnvelope",
    "InteropError",
    "canonical_json_bytes",
    "canonical_json_text",
    "parse_strict_json",
    "sha256_canonical",
    "validate_identifier",
    "validate_timestamp",
    "validate_version",
]
__version__ = "0.1.0"
