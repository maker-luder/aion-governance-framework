"""Bounded owner-governed execution infrastructure for AION/Astra candidates.

This package provides shared execution mechanics. It has no canonical write,
deployment, identity-mutation, or subjectivity-establishing capability.
"""

from .engine import AstraRuntime, BoundedExecutionEngine
from .models import IndividualRuntimeContext, RunResult, RunStatus, TaskSpec

__all__ = [
    "AstraRuntime",
    "BoundedExecutionEngine",
    "IndividualRuntimeContext",
    "RunResult",
    "RunStatus",
    "TaskSpec",
]
__version__ = "0.1.0"
