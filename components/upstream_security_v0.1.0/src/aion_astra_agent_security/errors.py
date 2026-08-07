class SecurityGovernanceError(Exception):
    """Base error for the candidate security governor."""


class ValidationError(SecurityGovernanceError):
    """Configuration or event violates a required invariant."""
