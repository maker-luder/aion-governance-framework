"""Fail-closed workbench exceptions."""


class WorkbenchError(Exception):
    """Base workbench error."""


class ValidationError(WorkbenchError):
    """Input or state is invalid."""


class ApprovalError(WorkbenchError):
    """Approval is missing, stale, mismatched or insufficient."""


class StateTransitionError(WorkbenchError):
    """Task state transition is prohibited."""


class WorkspaceBoundaryError(WorkbenchError):
    """A path or workspace operation crossed a configured boundary."""


class PatchError(WorkbenchError):
    """A candidate patch could not be applied atomically."""


class CommandPolicyError(WorkbenchError):
    """A command is outside the explicit local allowlist."""


class KernelDeniedError(WorkbenchError):
    """The Governance Kernel denied the operation."""


class AuditError(WorkbenchError):
    """Audit persistence or integrity failed."""


class EpisodicAdapterError(WorkbenchError):
    """Episodic provenance recording failed closed."""


class PackagingError(WorkbenchError):
    """Candidate packaging failed."""
