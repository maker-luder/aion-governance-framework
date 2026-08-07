"""Executable, owner-governed AION/Astra runtime candidate.

This package runs bounded candidate workflows.  It has no canonical write,
deployment, identity-mutation, or subjectivity-establishing capability.
"""

from .engine import AstraRuntime
from .models import RunResult, RunStatus, TaskSpec

__all__ = ["AstraRuntime", "RunResult", "RunStatus", "TaskSpec"]
__version__ = "0.1.0"

