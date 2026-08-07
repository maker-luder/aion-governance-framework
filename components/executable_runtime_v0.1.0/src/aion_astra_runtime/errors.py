"""Runtime-specific exceptions."""


class RuntimeCandidateError(Exception):
    """Base runtime candidate error."""


class PolicyDenied(RuntimeCandidateError):
    """Raised when a task or action violates the runtime policy."""


class PlannerFailure(RuntimeCandidateError):
    """Raised when a planner returns an invalid decision."""

