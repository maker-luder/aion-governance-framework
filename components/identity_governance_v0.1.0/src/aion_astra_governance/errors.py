class GovernanceError(Exception):
    """Base governance error."""


class ValidationError(GovernanceError):
    """Input violates a governance invariant."""


class ConflictError(GovernanceError):
    """An immutable identifier or output already exists."""
